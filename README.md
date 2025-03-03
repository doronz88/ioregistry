# ioregistry

Python library for IORegistry exploration.

## Installation

```shell
python3 -m pip install -U ioregistry
```

## Usage

See the following example as an example to query the associated USB-ethernet interface with a connected iDevice:

```python
from ioregistry.exceptions import IORegistryException
from ioregistry.ioentry import get_io_services_by_type

for ethernet_interface_entry in get_io_services_by_type('IOEthernetInterface'):
    try:
        apple_usb_ncm_data = ethernet_interface_entry.get_parent_by_type('IOService', 'AppleUSBNCMData')
    except IORegistryException:
        continue

    if 'waitBsdStart' in apple_usb_ncm_data.properties:
        # RSD interface
        continue

    try:
        usb_host = ethernet_interface_entry.get_parent_by_type('IOService', 'IOUSBHostDevice')
    except IORegistryException:
        continue

    product_name = usb_host.properties['USB Product Name']
    usb_serial_number = usb_host.properties['USB Serial Number']
    print(product_name, usb_serial_number, ethernet_interface_entry.name)
```
