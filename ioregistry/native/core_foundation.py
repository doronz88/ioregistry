import ctypes
from ctypes import c_bool, c_char_p, c_int32, c_long, c_uint32, c_void_p, cdll
from ctypes.util import find_library

CoreFoundation = cdll.LoadLibrary(find_library('CoreFoundation'))

kCFAllocatorDefault = c_void_p.in_dll(CoreFoundation, 'kCFAllocatorDefault')

# CFNumber type defines
kCFNumberSInt8Type = 1
kCFNumberSInt16Type = 2
kCFNumberSInt32Type = 3
kCFNumberSInt64Type = 4

kCFStringEncodingMacRoman = 0
kCFStringEncodingUTF8 = 0x08000100
kCFPropertyListXMLFormat_v1_0 = 100

CFTypeRef = c_void_p
CFStringRef = CFTypeRef
CFDictionaryRef = CFTypeRef
CFDataRef = CFTypeRef
CFAllocatorRef = CFTypeRef

CoreFoundation.CFStringCreateWithCString.argtypes = [c_void_p, c_char_p, c_int32]
CoreFoundation.CFStringCreateWithCString.restype = CFStringRef

CoreFoundation.CFStringGetCStringPtr.argtypes = [c_void_p, c_uint32]
CoreFoundation.CFStringGetCStringPtr.restype = c_char_p

CoreFoundation.CFStringGetCString.argtypes = [c_void_p, c_void_p, c_long, c_uint32]
CoreFoundation.CFStringGetCString.restype = c_bool

CoreFoundation.CFNumberGetValue.argtypes = [c_void_p, c_uint32, c_void_p]
CoreFoundation.CFNumberGetValue.restype = c_void_p

CoreFoundation.CFRelease.argtypes = [CFTypeRef]
CoreFoundation.CFRelease.restype = None

CoreFoundation.CFPropertyListCreateXMLData.argtypes = [CFAllocatorRef, CFTypeRef]
CoreFoundation.CFPropertyListCreateXMLData.restype = CFDataRef

CoreFoundation.CFDataGetLength.argtypes = [CFDataRef]
CoreFoundation.CFDataGetLength.restype = ctypes.c_long

CoreFoundation.CFDataGetBytePtr.argtypes = [CFDataRef]
CoreFoundation.CFDataGetBytePtr.restype = ctypes.POINTER(ctypes.c_uint8)


def CFSSTR(s: str) -> CFStringRef:
    """ Create CFString from Python string """
    return CoreFoundation.CFStringCreateWithCString(None, s.encode(), c_uint32(kCFStringEncodingUTF8))
