"""
file: ble_logger.py
author: Saifeddine ALOUI(ParisNeo) + ChatGPT
description: This script uses the Bleak library to discover and connect to a BLE device with a given MAC address,
then logs data from a specific service and characteristic of the device. The data is logged continuously if the characteristic has
a notification property, or read and printed once if the characteristic is read-only. The logged data is saved in a csv file with a
specified file path. The user can also specify a file header and the format of the data to be logged.
"""
import asyncio
import argparse
from bleak import discover, BleakClient
import struct 

def parse_data(data, entry_format='<Hiii'):
    """
        Parses the data received from the BLE device and returns a formatted string.
        
        :param data: The raw data received from the BLE device.
        :type data: bytes
        :param entry_format: The format of the data, defaults to '<Hiii' (little endian, short, 3 ints)
        :type entry_format: str
        :return: Formatted string of the parsed data
        :rtype: str
    """
    parsed_data = struct.unpack(entry_format, data)
    return ",".join([str(f) for f in parsed_data])


async def log_data(
                        address, 
                        service_uuid, 
                        characteristic_uuid, 
                        timeout, 
                        file_path, 
                        force_read=False,
                        file_header = "timestamp, acc_x, acc_y, acc_z",
                        entry_format='<Hiii'
                    ):
    """
        Logs data from a specific characteristic of a BLE device with a given address, service UUID and characteristic UUID, and timeout.
        If the characteristic has a notification property, the data is logged continuously until the user press 'q'
        If the characteristic is read-only, the data is read and printed once, then disconnected.
        If the characteristic is write-only, the user is told that it can't be used for logging.
        
        :param address: The MAC address of the device.
        :type address: str
        :param service_uuid: The UUID of the service that the characteristic belongs to.
        :type service_uuid: str
        :param characteristic_uuid: The UUID of the characteristic to log data from.
        :type characteristic_uuid: str
        :param timeout: The timeout in seconds for the BLE device to respond.
        :type timeout: float
        :param file_path: The path to the csv log file to be created
        :type file_path: str
        :param force_read: if set to True the script will read the characteristic instead of subscribing to notifications, defaults to False
        :type force_read: bool
        :param file_header: The header of the csv file, defaults to "timestamp, acc_x, acc_y, acc_z"
        :type file_header: str
        :param entry_format: The format of the data, defaults to '<Hiii' (little endian, short, 3 ints)
        :type entry_format: str
    """

    try:
        print("scanning...",end="")
        devices = await discover(timeout=timeout)
        device = next((d for d in devices if d.address.lower() == address.lower()), None)
        if device and device.address==address:
            print(f"OK\ndevice found : {device.name} : {device.address}")
            print(f"Creating device...",end="")
            try:                
                async with BleakClient(device.address) as client:
                    print("OK")
                    print("connecting...",end="")
                    try:
                        #await client.connect()#timeout=timeout)
                        print("OK")
                        services = await client.get_services()
                        service = next((s for s in services if s.uuid == service_uuid), None)
                        characteristic = next((c for c in service.characteristics if c.uuid == characteristic_uuid), None)
                        f = open(file_path,"w")
                        f.write(file_header+"\n")
                        if "notify" in characteristic.properties:
                            if force_read:
                                nb_received = 1
                                print("Logging in polling mode.\nTo exit press Ctrl + C")
                                while True:
                                    data = await client.read_gatt_char(characteristic)
                                    parsed = parse_data(data, entry_format)
                                    f.write(parsed)
                                    print(f"Logged {nb_received} entries", end='\r')
                                    nb_received += 1
                            else:
                                nb_received = 1
                                def data_received(_, data):
                                    f.write(parse_data(data))
                                    print(f"Logged {nb_received} entries", end='\r')
                                    nb_received += 1

                                await client.start_notify(characteristic.uuid, data_received)
                                print("Logging in notification mode.\n")
                                while True:
                                    user_input = input("Press 'q' to stop logging data: ")
                                    if user_input.lower() == "q":
                                        break
                                await client.stop_notify(characteristic.uuid)
                                await client.disconnect()
                        elif "read" in characteristic.properties:
                            data = await client.read_gatt_char(characteristic)
                            print("Data received: {}".format(data))
                            await client.disconnect()
                        elif "write" in characteristic.properties:
                            print("This characteristic is write-only, it can't be used for logging.")
                            await client.disconnect()
                        else:
                            print("This characteristic has no read or notify properties, it can't be used for logging.")
                            await client.disconnect()
                        f.close()
                    except Exception as e:
                        print(f"NOK")
                        print(f"Failed to connect to the device: {e}")
                        return
            except Exception as e:
                print(f"NOK")
                print(f"Failed to connect to the device: {e}")
                return

    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
Logs data from a specific characteristic of a BLE device with a given address,
service UUID and characteristic UUID, and timeout. If the characteristic has a
notification property, the data is logged continuously until the user press 'q'
If the characteristic is read-only, the data is read and printed once, then
disconnected. If the characteristic is write-only, the user is told that it can't
be used for logging.    
    """)
    parser.add_argument("mac_address", help="MAC address of the device")
    parser.add_argument("service_uuid", help="UUID of the service that the characteristic belongs to")
    parser.add_argument("characteristic_uuid", help="UUID of the characteristic to log data from")
    parser.add_argument("-p", "--path", help="Path to the csv file to be created",default="./log.csv")
    parser.add_argument("-t", "--timeout", help="Timeout in seconds", type=float, default=15.0)
    parser.add_argument("-f", "--force_read", help="Force using read instead of notify", action="store_true")
    parser.add_argument("-H", "--file_header", help="The header of the csv file, defaults to 'timestamp, acc_x, acc_y, acc_z'", default="timestamp, acc_x, acc_y, acc_z")
    parser.add_argument("-F", "--entry_format", help="The format of the data, defaults to '<Hiii' (little endian, short, 3 ints)", default="<Hiii")
    args = parser.parse_args()

    print(f"Searching for :\n    Mac address:{args.mac_address}\n    Service UUID:{args.service_uuid}\n    Characteristic uuid:{args.characteristic_uuid}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(log_data(args.mac_address, args.service_uuid, args.characteristic_uuid, args.timeout, args.path, args.force_read,args.file_header, args.entry_format))

