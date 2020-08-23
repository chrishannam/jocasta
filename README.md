# Jocasta
Library to extract data from serial and send it various services.

# Quick Start
## Basic Home Config File
Create a directory in your home directory to store the config file. You can pass in a file
at run time but this is the quick start.

```
cd ~
mkdir .config
cd .config
```

Create a file called `jocasta_config.ini` and copy and paste the following into the depending on which services you want.

```
[io_adafruit]
username = username
key = key
feeds = temperature,light,humidity
measurements = temperature,light,humidity

[influxdb]
host = 192.168.1.100
port = 8086
password = admin
username = admin
database = greenhouses

[file_system]
file_name = /tmp/sensor_data.json

[temperature_ranges]
maximum = 55.0
minimum = -10.0
```

## Running
Start `jocasta` by add the path of your serial device.

### OSX
Command and output
```
$ jocasta /dev/tty.usbserial-14230
╒═════════════╤══════════╤══════════╤══════════╤════════╕
│ Temperature │ Location │ Moisture │ Humidity │ Light  │
├─────────────┼──────────┼──────────┼──────────┼────────┤
│ 23.2        │ office   │ 568      │ 61.2     │ 5800.0 │
╘═════════════╧══════════╧══════════╧══════════╧════════╛
```

###  Raspberry Pi / Linux
Command and output
```
$ jocasta /dev/ttyUSB0
╒═════════════╤══════════╤══════════╤══════════╤════════╕
│ Temperature │ Location │ Moisture │ Humidity │ Light  │
├─────────────┼──────────┼──────────┼──────────┼────────┤
│ 23.2        │ office   │ 568      │ 61.2     │ 5800.0 │
╘═════════════╧══════════╧══════════╧══════════╧════════╛
```

# Supported Services
Services and things Jocasta can send data to.

## InfluxDB - https://www.influxdata.com
### Config
Add the following to your `jocasta-config.ini` file, making sure you update the values
to match your InfluxDB server.
```
[influxdb]
host = 192.168.1.100
port = 8086
password = admin
username = admin
database = greenhouses
```

## Adafruit IO - https://io.adafruit.com
```
[io_adafruit]
username = username
key = key
feeds = temperature,light,humidity
measurements = temperature,light,humidity
```

## File System
```
[file_system]
file_name = /tmp/sensor_data.json
```
