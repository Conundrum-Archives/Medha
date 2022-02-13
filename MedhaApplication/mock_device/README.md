# Mock Device Module

This module is a mock module for simulating (or mocking) actual device_controller module. The device controller module is a program that runs on local device (eg: Medha Rover on board) and acts as interface for application module.

This mock module is useful if you are working on application which requires to talk to device API's and get data.

## How to setup

(optional)
before proceeding make sure to create seperate virtual environment for mock as this module is only for mocking and not part of main functionality.

```bash
python -m venv venv
venv/Scripts/activate       # if WINDOWS
source ./venv/bin/activate  # of LINUX
```

start to set up mock device module.

Install necessary python dependencies and run the program.

```bash
pip install -r mock_requirements.txt
```

Run the mock_device_controller.py program

```bash
python mock_device_controller.py
```


Note: The mock API will be running on your system IP (or localhost) with port 5000.


Once running you will see something of this log (ip address may vary as per your network configuration)

```bash
* Running on http://192.168.0.100:5000/ (Press CTRL+C to quit)
```


## Endpoints

available mocked end points:

----

- /
  API home or base url

----

- /setServoAngle/$servoname

  (URL parameter) **$servoname**: BaseServo or UpperServo
  (QUERY parameter) **angle**: value from 0 to 359
  
  API to set respective servo angle

----

- /captureImage
  API to capture image and return base64 format

----

- /getDistance
  API to get distance from USS sensor

----