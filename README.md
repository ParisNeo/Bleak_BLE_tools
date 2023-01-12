# BLE Data Logger

[![GitHub release](https://badgen.net/github/release/ParisNeo/Bleak_BLE_tools)](https://github.com/ParisNeo/Bleak_BLE_tools/releases)
[![GitHub license](https://badgen.net/github/license/ParisNeo/Bleak_BLE_tools)](https://github.com/ParisNeo/Bleak_BLE_tools/blob/master/LICENSE)

File: logger.py

Author: Saifeddine ALOUI + ChatGPT
## Description
This script uses the Bleak library to connect to a BLE device and logs data from a specific characteristic of the device. The logged data is saved to a CSV file. The script supports two modes:

Notification mode: The script subscribes to notifications from the characteristic and logs the data as it is received. The logging can be stopped by pressing 'q'.
Polling mode: The script periodically reads the characteristic and logs the data. This mode can be used when the characteristic does not support notifications.
Installation
The script requires the following libraries:

- asyncio
- argparse
- bleak
- struct
To install these libraries, use the following command:

```bash
pip install asyncio argparse bleak struct
```
## Usage
The script can be run from the command line by providing the following arguments:

- mac_address: The MAC address of the device.
- service_uuid: The UUID of the service that the characteristic belongs to.
- characteristic_uuid: The UUID of the characteristic to log data from.
- -p, --path: The path to the CSV file to be created. Default is ./log.csv.
- -t, --timeout: The timeout in seconds for the BLE device to respond. Default is 5.0.
- -f, --force_read: Forces the script to use polling mode even if the characteristic supports notifications.
- -e, --entry_format: The format of the data, defaults to '<Hiii' (little endian, short, 3 ints)
- -h, --file_header: The header of the csv file, defaults to "timestamp, acc_x, acc_y, acc_z"

```bash
python logger.py <mac_address> <service_uuid> <characteristic_uuid> [-p <file_path>] [-t <timeout>] [-f] [-e <entry_format>] [-h <file_header>]
```

## Customization explaining
The end user can control the file header and the data format through the call arguments of the script logger.py. The arguments file_header and entry_format allow the user to specify the format of the data and the header of the csv file respectively.

For example, if the user wants to log data from a temperature sensor that sends data in the format of a float in degrees Celsius, the user can set file_header to "timestamp, temperature (C)" and entry_format to '<Hf' (little endian, short, float). Assuming a service uuid of 1234 and characteristic 5678, the user can then run the script with these arguments:
```bash
python logger.py -a "AA:BB:CC:DD:EE:FF" "1234" "5678" -p "./temperature.csv" -H "timestamp, temperature (C)" -F '<Hf'
```
Another example, if the user wants to log data from an accelerometer sensor that sends data in the format of 3 integers representing the X, Y, and Z axis values respectively, the user can set file_header to "timestamp, acc_x, acc_y, acc_z" and entry_format to '<Hiii' (little endian, short, 3 ints). The user can then run the script with these arguments:

```bash
python logger.py -a "AA:BB:CC:DD:EE:FF" "1234" "5678" -p "./accelerometer.csv" -H "timestamp, acc_x, acc_y, acc_z" -F '<Hiii'
```

It is important to note that the entry_format argument should be set according to the data format of the sensor and the file_header argument should match the format of the data in the entry_format argument.

## Other examples
Log data from the accelerometer that sends data in format timestamp:uint16,accx:int32,accy:int32,accz:int32 through service (UUID: 0xABCD)  characteristic (UUID: 0xABCD) of a device with MAC address 12:34:56:78:90:AB and save the data to ./accelerometer.csv:
```bash
python logger.py 12:34:56:78:90:AB 0xABCD 0xABCD  -p ./accelerometer.csv -H "timestamp, acc_x, acc_y, acc_z" -F "<Hiii"
```

## Note
`For some devices, the notification mode may not work. In this case, you can use the polling mode by adding -f to the request. This will force using the read method instead of notification.`


## Exeting the application
To exit the application, you just need to press q.

