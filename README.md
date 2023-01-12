# BLE Data Logger
File: logger.py
Author: Saifeddine ALOUI + ChatGPT
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
# Examples
Log data from the accelerometer characteristic (UUID: 0xABCD) of a device with MAC address 12:34:56:78:90:AB and save the data to ./accelerometer.csv:
```bash
python logger.py 12:34:56
```
