# Jocasta
Library to extract data from serial devices and send it various services.

`jocasta` is used to read JSON output from a serially attached device and relay it to a
another service. For example a database or a local csv file.

Example Arduino code can be found here [Sensors_Basic](arduino/Sensors_Basic). This is a simple
sketch designed to read data from a number of cheap available sensors and return the readings over USB serial
as a JSON string.

# Quick Start
## Installation
`pip install jocasta` or use `sudo` to install system wide.

## Config File (Optional)
Create a directory in your home directory to store the config file.

```
cd ~
mkdir .config
cd .config
```

Create a file called `jocasta_config.ini` and copy and paste the following into the depending on which services you want.

```
[csv_file]
path = /tmp/sensor_data.csv

[file_system]
file_name = /tmp/sensor_data.json

[influxdb]
host = 192.168.1.100
port = 8086
password = admin
username = admin
database = greenhouses

[io_adafruit]
username = your_username
key = your_key
# change to match your configured feeds on https://io.adafruit.com
feeds = office.office-temperature,office.office-light,office.office-humidity
# field names in your JSON payload from your sensor
measurements = temperature,light,humidity

[temperature_ranges]
maximum = 55.0
minimum = -10.0
```

The last section `temperature_ranges` is a range you add to ensure if your reading called
`temperature` is outside of the values stated it will be ignored.
This was added specifically as the `ds18b20` sensor can report very large or small numbers when
reporting an issue.

## Running
Start `jocasta` by add the path of your serial device. This path can be found from looking in rhe `/dev`
directory on both OSX and Linux.

### OSX
The USB device will typically be locate in `/dev` with a name that starts `tty.`

```
$ jocasta -p /dev/tty.usbserial-14230
╒═════════════╤══════════╤══════════╤══════════╤════════╕
│ Temperature │ Location │ Moisture │ Humidity │ Light  │
├─────────────┼──────────┼──────────┼──────────┼────────┤
│ 23.2        │ office   │ 568      │ 61.2     │ 5800.0 │
╘═════════════╧══════════╧══════════╧══════════╧════════╛
```

###  Raspberry Pi / Linux
The USB device will typically be locate in `/dev` with a name that starts `ttyUSB`

```
$ jocasta -p /dev/ttyUSB0
╒═════════════╤══════════╤══════════╤══════════╤════════╕
│ Temperature │ Location │ Moisture │ Humidity │ Light  │
├─────────────┼──────────┼──────────┼──────────┼────────┤
│ 23.2        │ office   │ 568      │ 61.2     │ 5800.0 │
╘═════════════╧══════════╧══════════╧══════════╧════════╛
```

# Running
A config file can supplied to the command line call using `-c`:
```
$ jocasta -p /dev/tty.usbserial-14230 -c /path/to/config.ini
```

# Supported Services
Services and things Jocasta can send data to.

## Adafruit IO - https://io.adafruit.com
Adafruit's beta IoT hosted application.

### Config
```
[io_adafruit]
username = username
key = key
feeds = temperature,light,humidity
measurements = temperature,light,humidity
```

## CSV File
Outputs as `csv` to a file on disk. This is handy for other applications to access the data.

### Config
```
[csv_file]
path = /tmp/sensor_data.csv
```

## File System
Outputs `json` to a file on disk. This is handy for other applications to access the data. New readings
are appended to the file.

### Config
```
[file_system]
file_name = /tmp/sensor_data.json
```

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
