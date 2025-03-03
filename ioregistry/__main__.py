import click

from ioregistry.exceptions import IORegistryException
from ioregistry.ioentry import get_io_services_by_type


@click.command()
def cli():
    services = get_io_services_by_type('IOEthernetInterface')
    for service in services:
        try:
            apple_usb_ncm_data = service.get_parent_by_type('AppleUSBNCMData', 'IOService')
        except IORegistryException:
            continue
        print(service, apple_usb_ncm_data, apple_usb_ncm_data.properties)
        # print(apple_usb_ncm_data.properties)


# test
if __name__ == '__main__':
    cli()
