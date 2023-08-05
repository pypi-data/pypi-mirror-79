# Boon Amber Python SDK

An SDK for Boon Amber sensor analytics

- __Website__: [boonlogic.com](https://boonlogic.com)
- __Documentation__: [Boon Docs Main Page](https://docs.boonlogic.com)
- __SDK Functional Breakdown__: [amber-python-sdk classes and methods](docs/boonamber/index.html)

## Installation

The Boon Amber SDK is a Python 3 project and can be installed via pip.

```
pip install boonamber
```

## Credentials setup

Note: An account in the Boon Amber cloud must be obtained from Boon Logic to use the Amber SDK.

The username and password should be placed in a file named _~/.Amber.license_ whose contents are the following:

```
{
    "default": {
        "username": "AMBER-ACCOUNT-USERNAME",
        "password": "AMBER-ACCOUNT-PASSWORD"
        "server": "https://amber.boonlogic.com/v1"
    }
}
```

The _~/.Amber.license_ file will be consulted by the Amber SDK to find and authenticate your account credentials with the Amber server. Credentials may optionally be provided instead via the environment variables `AMBER_USERNAME` and `AMBER_PASSWORD`.

## Connectivity test

The following Python script provides a basic proof-of-connectivity:

[connect-example.py](examples/connect-example.py)

```
from boonamber import AmberClient

# At initialization the client discovers Amber account credentials
# under the "default" entry in the ~/.Amber.license file.
amber = AmberClient()

sensors = amber.list_sensors()
print("sensors: {}".format(sensors))
```

Running the connect-example.py script should yield output like the following:
```
$ python connect-example.py
sensors: {}
```
where the dictionary `{}` lists all sensors that currently exist under the given Boon Amber account.

## Full Example

The following Python script will demonstrate each API call in the Amber Python SDK.

[full-example.py](examples/full-example.py)

```
import sys
from boonamber import AmberClient, AmberCloudError, AmberUserError

"""Demonstrates usage of all Amber SDK endpoints."""

# connect with default license
# use 'license_id=<name>' to specify something other than 'default'
amber = AmberClient()

# List all sensors belonging to current user
print("listing sensors")
try:
    sensors = amber.list_sensors()
except AmberCloudError as e:
    print(e)
    sys.exit(1)
except AmberUserError as e:
    print(e)
    sys.exit(1)
print("sensors: {}".format(sensors))
print()

# Create a new sensor
print("creating sensor")
try:
    sensor_id = amber.create_sensor('new-test-sensor')
except AmberCloudError as e:
    print(e)
    sys.exit(1)
except AmberUserError as e:
    print(e)
    sys.exit(1)
print("sensor-id: {}".format(sensor_id))
print()

# Get sensor info
print("getting sensor")
try:
    sensor = amber.get_sensor(sensor_id)
except AmberCloudError as e:
    print("Amber Cloud error: {}".format(e))
    sys.exit(1)
except AmberUserError as e:
    print("Amber user error: {}".format(e))
    sys.exit(1)
print("sensor: {}".format(sensor))
print()

# Update the label of a sensor
print("updating label")
try:
    label = amber.update_label(sensor_id, 'test-sensor')
except AmberCloudError as e:
    print("Amber Cloud error: {}".format(e))
    sys.exit(1)
except AmberUserError as e:
    print("Amber user error: {}".format(e))
    sys.exit(1)
print("label: {}".format(label))
print()

# Configure a sensor
print("configuring sensor")
try:
    config = amber.configure_sensor(sensor_id, feature_count=1, streaming_window_size=25)
except AmberCloudError as e:
    print("Amber Cloud error: {}".format(e))
    sys.exit(1)
except AmberUserError as e:
    print("Amber user error: {}".format(e))
    sys.exit(1)
print("config: {}".format(config))
print()

# Get sensor configuration
print("getting configuration")
try:
    config = amber.get_config(sensor_id)
except AmberCloudError as e:
    print("Amber Cloud error: {}".format(e))
    sys.exit(1)
except AmberUserError as e:
    print("Amber user error: {}".format(e))
    sys.exit(1)
print("config: {}".format(config))
print()

# Stream data to a sensor
print("streaming data")
data = [0, 1, 2, 3, 4]
try:
    results = amber.stream_sensor(sensor_id, data)
except AmberCloudError as e:
    print("Amber Cloud error: {}".format(e))
    sys.exit(1)
except AmberUserError as e:
    print("Amber user error: {}".format(e))
    sys.exit(1)
print("results: {},".format(results))
print()

# Get clustering status from a sensor
print("getting status")
try:
    status = amber.get_status(sensor_id)
except AmberCloudError as e:
    print("Amber Cloud error: {}".format(e))
    sys.exit(1)
except AmberUserError as e:
    print("Amber user error: {}".format(e))
    sys.exit(1)
print("status: {}".format(status))
print()

# Delete a sensor instance
print("deleting sensor")
try:
    amber.delete_sensor(sensor_id)
except AmberCloudError as e:
    print("Amber Cloud error: {}".format(e))
    sys.exit(1)
except AmberUserError as e:
    print("Amber user error: {}".format(e))
    sys.exit(1)
print("succeeded")
print()
```

## Sample CSV file processor

The following will process a file named data.csv residing in the current working directory of this Python script.  Each row will be fed to an Amber instance with SI analytics being displayed.

[stream-example.py](examples/stream-example.py)<br>
[data.csv](examples/data.csv)

```
import csv
import sys
from boonamber import AmberClient, AmberCloudError

"""Demonstrates a streaming use case in which we read continuously
   from a CSV file, inference the data line by line, and print results.
"""

amber = AmberClient()

sensor_id = 'put-created-sensor-id-here'

# The commented out block below creates a new sensor and prints the
# corresponding sensor ID. These lines should be uncommented the first
# time this script is run to create the sensor which is used for this
# example. For any following runs, these lines should be commented out
# again and the created sensor ID should be filled into the line above
# so that the same sensor is accessed on subsequent runs.

# try:
#     sensor_id = amber.create_sensor(label='stream-example-sensor')
# except AmberCloudError as e:
#     print(e)
#     sys.exit(1)
# print("created sensor {}".format(sensor_id))

print("using sensor {}".format(sensor_id))

# Configure the sensor: feature_count is 3 since our CSV data has three columns
try:
    config = amber.configure_sensor(sensor_id, feature_count=3, streaming_window_size=25)
except AmberCloudError as e:
    print(e)
    sys.exit(1)
print("config: {}".format(config))

# Open data file and begin streaming!
with open('data.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')

    for row in reader:
        data = [float(d) for d in row]

        try:
            result = amber.stream_sensor(sensor_id, data)
        except AmberCloudError as e:
            print(e)
            sys.exit(1)

        state = result['state']
        anomaly_index = result['SI'][0]

        data_pretty = ' '.join("{:5.2f}".format(d) for d in data)
        print("{} [{}] -> {}".format(state, data_pretty, anomaly_index))
```