"""
file: device_services_lister.py
author: ALOUI Saifeddine (ParisNeo) + chatgpt
description: This script uses the Bleak library to discover and connect to a BLE device with a given MAC address, 
then lists all the services and characteristics of the device and their properties (read, write, notify).
"""
import asyncio
import argparse
from bleak import discover, BleakClient

async def list_services_and_characteristics(address, timeout):
    """
    Lists all services and characteristics of a BLE device with a given address and timeout.
    
    :param address: The MAC address of the device.
    :type address: str
    :param timeout: The timeout in seconds for the BLE device to respond.
    :type timeout: float
    """
    try:
        devices = await discover(timeout=timeout)
        found = False
        for device in devices:
            if device and (device.address==address or address==""):
                found=True
                print(f"\n\n -------- device found ----")
                print(f"Name: {device.name}")
                print(f"Mac address : {device.address}")
                try:
                    async with BleakClient(device.address) as client:
                        services = await client.get_services()
                        for service in services:
                            print("Service: {} - {}".format(service.uuid, service.description))
                            for characteristic in service.characteristics:
                                # Print characteristic properties
                                properties = []
                                if "read" in characteristic.properties:
                                    properties.append("read")
                                if "write" in characteristic.properties:
                                    properties.append("write")
                                if "notify" in characteristic.properties:
                                    properties.append("notify")
                                print("  Characteristic: {} - {} - {}".format(characteristic.uuid, characteristic.description, properties))
                        await client.disconnect()
                except Exception as e:
                    print(f"NOK")
                    print(f"Failed to connect to the device: {e}")
                    
        if found==False:
            print(f"Device with address `{address}` not found")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m","--mac_address", help="MAC address of the device", type=str, default="")
    parser.add_argument("-t", "--timeout", help="Timeout in seconds", type=float, default=5.0)
    args = parser.parse_args()
    print(f'Searching for devices with mac address :`{args.mac_address}`')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(list_services_and_characteristics(args.mac_address, args.timeout))
