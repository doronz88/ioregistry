import ctypes
from ctypes import c_int, c_uint, c_uint32, c_void_p, cdll
from ctypes.util import find_library

from ioregistry.native.core_foundation import CFDictionaryRef

IOKit = cdll.LoadLibrary(find_library('IOKit'))
# kIOMasterPortDefault is no longer exported in BigSur but no biggie, using NULL works just the same
kIOMasterPortDefault = 0  # WAS: c_void_p.in_dll(iokit, "kIOMasterPortDefault")

# `io_name_t` defined as `typedef char io_name_t[128];`
# in `device/device_types.h`
io_name_size = 128
io_registry_entry_t = c_uint

# defined in `mach/kern_return.h`
KERN_SUCCESS = 0
# kern_return_t defined as `typedef int kern_return_t;` in `mach/i386/kern_return.h`
kern_return_t = c_int

IOKit.IOServiceMatching.restype = c_void_p

IOKit.IOIteratorNext.argtypes = [c_void_p]
IOKit.IOIteratorNext.restype = io_registry_entry_t

IOKit.IOServiceGetMatchingServices.argtypes = [c_void_p, c_void_p, c_void_p]
IOKit.IOServiceGetMatchingServices.restype = kern_return_t

IOKit.IORegistryEntryGetParentEntry.argtypes = [io_registry_entry_t, c_void_p, ctypes.POINTER(io_registry_entry_t)]
IOKit.IOServiceGetMatchingServices.restype = kern_return_t

IOKit.IORegistryEntryCreateCFProperty.argtypes = [ctypes.POINTER(io_registry_entry_t), c_void_p, c_void_p, c_uint32]
IOKit.IORegistryEntryCreateCFProperty.restype = c_void_p

IOKit.IORegistryEntryCreateCFProperties.argtypes = [io_registry_entry_t,
                                                    ctypes.POINTER(CFDictionaryRef),
                                                    c_void_p,
                                                    c_uint32]
IOKit.IORegistryEntryCreateCFProperties.restype = c_int

IOKit.IORegistryEntryGetPath.argtypes = [c_void_p, c_void_p, c_void_p]
IOKit.IORegistryEntryGetPath.restype = kern_return_t

IOKit.IORegistryEntryGetName.argtypes = [io_registry_entry_t, c_void_p]
IOKit.IORegistryEntryGetName.restype = kern_return_t

IOKit.IOObjectGetClass.argtypes = [io_registry_entry_t, c_void_p]
IOKit.IOObjectGetClass.restype = kern_return_t

IOKit.IOObjectRelease.argtypes = [c_void_p]
