import ctypes
import plistlib
from typing import Generator

from ioregistry.allocated import Allocated
from ioregistry.exceptions import IORegistryException
from ioregistry.native.core_foundation import CFTypeRef, CoreFoundation
from ioregistry.native.iokit import KERN_SUCCESS, IOKit, io_iterator_t, io_name_size, io_registry_entry_t, \
    kIOMasterPortDefault


def get_io_entry_class_name(entry: io_registry_entry_t) -> str:
    """ Get the name of the given IO Entry class """
    classname = ctypes.create_string_buffer(io_name_size)
    IOKit.IOObjectGetClass(entry, ctypes.byref(classname))
    return classname.value


def convert_cf_native_to_python(cf_object: CFTypeRef) -> dict:
    """ Create a python object from a given native CoreFoundation object """

    # Create a temporary XML property list
    xml_data = CoreFoundation.CFPropertyListCreateXMLData(None, cf_object)

    # Get the size and pointer to the data
    data_length = CoreFoundation.CFDataGetLength(xml_data)
    data_ptr = CoreFoundation.CFDataGetBytePtr(xml_data)

    # Create a Python bytes object from the data
    bytes_data = ctypes.string_at(data_ptr, data_length)

    # Convert bytes to Python dictionary using plistlib
    result = plistlib.loads(bytes_data)

    # Release CF objects
    CoreFoundation.CFRelease(xml_data)

    return result


class IOEntry(Allocated):
    def __init__(self, entry: io_registry_entry_t) -> None:
        super().__init__()
        self._entry = entry

    @property
    def name(self) -> str:
        """ Get the name of the given IO Entry """

        name = ctypes.create_string_buffer(io_name_size)
        error = IOKit.IORegistryEntryGetName(self._entry, ctypes.byref(name))
        if error != KERN_SUCCESS:
            raise IORegistryException(f'Failed to get name: {error}')
        return name.value.decode()

    @property
    def properties(self) -> dict:
        """ Get entry properties using `IORegistryEntryCreateCFProperties()` """

        # Create a pointer to hold the dictionary
        props = ctypes.c_void_p()

        # Call IORegistryEntryCreateCFProperties
        kr = IOKit.IORegistryEntryCreateCFProperties(self._entry, ctypes.byref(props), None, 0)

        if kr != 0:
            # Release the entry and return None if there was an error
            IOKit.IOObjectRelease(self._entry)
            raise IORegistryException(f'Failed to create properties: {kr}')

        # Convert the properties to a Python dictionary
        result = convert_cf_native_to_python(props)

        # Release CF object
        CoreFoundation.CFRelease(props)

        return result

    def get_parent_by_type(self, plane: str, parent_type: str) -> 'IOEntry':
        """ Walk up the IOService tree in look for the given type """
        entry = self._entry
        parent_type = parent_type.encode()
        while get_io_entry_class_name(entry) != parent_type:
            parent = io_registry_entry_t()
            error = IOKit.IORegistryEntryGetParentEntry(entry, plane.encode(), ctypes.byref(parent))
            # If we weren't able to find a parent for the device, we're done.
            if error != KERN_SUCCESS:
                raise IORegistryException(f'Failed to get parent: {error}')
            entry = parent
        return IOEntry(entry)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} NAME:{self.name}>'

    def _deallocate(self) -> None:
        IOKit.IOObjectRelease(self._entry)


def get_io_services_by_type(service_type: str) -> Generator[IOEntry, None, None]:
    """ Returns iterator for specified `service_type` """
    interator = io_iterator_t()

    error = IOKit.IOServiceGetMatchingServices(
        kIOMasterPortDefault,
        IOKit.IOServiceMatching(service_type.encode('utf-8')),
        ctypes.byref(interator))

    if error != KERN_SUCCESS:
        raise IORegistryException(f'Failed to get services: {error}')

    while IOKit.IOIteratorIsValid(interator):
        entry = IOKit.IOIteratorNext(interator)
        if not entry:
            break
        yield IOEntry(entry)
    IOKit.IOObjectRelease(interator)
