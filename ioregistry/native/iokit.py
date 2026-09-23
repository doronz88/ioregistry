import ctypes
from ctypes import c_char_p, c_int, c_uint, c_uint32, c_void_p

from ioregistry.native.core_foundation import CFDictionaryRef, load_framework

IOKit = load_framework('IOKit')

kIOMasterPortDefault = 0
natural_t = c_uint32
mach_port_t = natural_t
io_object_t = mach_port_t
io_iterator_t = io_object_t
io_name_size = 128
io_registry_entry_t = c_uint
KERN_SUCCESS = 0
IOOptionBits = c_uint32
kern_return_t = c_int

IOKit.IOIteratorNext.argtypes = [c_void_p]
IOKit.IOServiceMatching.restype = ctypes.POINTER(CFDictionaryRef)

IOKit.IOIteratorNext.argtypes = [io_iterator_t]
IOKit.IOIteratorNext.restype = io_registry_entry_t

IOKit.IOServiceGetMatchingServices.argtypes = [mach_port_t, CFDictionaryRef, ctypes.POINTER(io_iterator_t)]
IOKit.IOServiceGetMatchingServices.restype = kern_return_t

IOKit.IORegistryEntryGetParentEntry.argtypes = [io_registry_entry_t, c_void_p, ctypes.POINTER(io_registry_entry_t)]
IOKit.IORegistryEntryGetParentEntry.restype = kern_return_t

IOKit.IORegistryEntryCreateCFProperties.argtypes = [io_registry_entry_t,
                                                    ctypes.POINTER(CFDictionaryRef),
                                                    c_void_p,
                                                    IOOptionBits]
IOKit.IORegistryEntryCreateCFProperties.restype = kern_return_t

IOKit.IORegistryEntryGetName.argtypes = [io_registry_entry_t, c_void_p]
IOKit.IORegistryEntryGetName.restype = kern_return_t

IOKit.IOObjectGetClass.argtypes = [io_registry_entry_t, c_void_p]
IOKit.IOObjectGetClass.restype = kern_return_t

IOKit.IOObjectConformsTo.argtypes = [io_object_t, c_char_p]
IOKit.IOObjectConformsTo.restype = c_uint

IOKit.IOObjectRelease.argtypes = [io_object_t]
IOKit.IOObjectRelease.restype = kern_return_t
