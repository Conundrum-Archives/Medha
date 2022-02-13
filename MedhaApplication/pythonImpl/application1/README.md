# Application1

This application is also called as 180_180_dome application. It can capture distance using ultrasonic sensor and/or camera image of the top dome view of the robot.

## Configuration

configuration can be found in parent directory of this application:

- MedhaApplication (folder)
  - pythonImple (folder)
    - application1 (folder)
    - Utils (folder)
    - **config.json** (file)
    - other stuff

**application1** section in config.json is only related to application1

make sure you do not alter json structure and modify values as applicable

----

- **data_dir**: provide a directory name to save collectd data as part of application1.py
(make sure name follows standard folder naming conventions-no space, no special characetrs, etc)

----

- **clean_data_dir_always**: true or false
Explanation: if true, it will clean the old data_dir folder

----

- **scan_config**: scan related configurations

  - **baseservo_start_angle**: starting angle for baseservo to start scanning
  preffered value: 0

  - **upperservo_start_angle**: starting angle for upperservo to start scanning
  preffered value: 0

  - **baseservo_sampling**: provide value to increment base servo angle with this value.
  Example:

    if value is 10, then base servo will scan for angles 0, 10, 20, 20, ...
    
    if value is 20, then base servo will scan for angles 0, 20, 40, ...

  - **upperservo_sampling**: provide value to increment upper servo angle with this value.
  Example:

    if value is 10, then upper servo will scan for angles 0, 10, 20, 20, ...
    
    if value is 20, then upper servo will scan for angles 0, 20, 40, ...

  - **proceed_always**: true or false
  Explanation: if set to true, scanner will prompt weather to proceed for next step or retry the same operation.
  Example: if there is glitch is reading distance value or servo has pulse glitch while setting to an angle, setting this key to true would be helpful rather than restarting entire scan from first

    **Note**: proceed_always if set to true, will keep prompting for every device level opertaions it does (getting distance, setting servo, etc).

----

- **operating_device**: configurations related to device/robot that you be operating on.

  - **base_url**: url to communicate to the device or robot running local-controller
  Example: if your robot is running MedhaBoard module and having network ip address of 192.168.0.100 and port 5000 then provide as http://192.168.0.100:5000

    **Note**: if running mock-controller: provide mock device host:port. eg: http://localhost:5000

  - **modules**: modules that are connected to your robot and configurations related to them.
    Syntax: 
      "modulename": {
        "enabled": true or false
        -- other configurations --
      }

    **Note**: few points to note:
    * baseservo and upperservo must be enabled (enables=true) for application1
    * provide min_angle and max_angle respectively for each servos. Usually 0 and 180 respectively
    * if you have camera module configured, set enabled=true for camera module section
    * for camera, makesure capture_settings resWidth and resHeight are as per your camera resolution else enter MAX as value to take highest avalable resolution. Also getbase64 is true as application needs to read captured image from device.

----

- **end_points**: device endpoints for application to utilize. (Can keep them default)

----

## sample configuration

```json
{
  "application1": {
    "data_dir": "datadir",
    "clean_data_dir_always": true,
    "scan_config": {
      "baseservo_start_angle": 0,
      "upperservo_start_angle": 0,
      "baseservo_sampling": 20,
      "upperservo_sampling": 30,
      "proceed_always": true
    },
    "operating_device": {
      "base_url": "http://192.168.0.100:5000",
      "modules": {
        "baseservo": {
          "enabled": true,
          "min_angle": 0,
          "max_angle": 180
        },
        "upperservo": {
          "enabled": true,
          "min_angle": 0,
          "max_angle": 180
        },
        "camera": {
          "enabled": true,
          "capture_settings": {
            "resWidth": "1920",
            "resHeight": "1080",
            "rotate": "0",
            "captureFile": "capture.jpg",
            "getbase64": "true"
          }
        }
      },
      "end_points": {
        "baseservo": "/setServoAngle/BaseServo",
        "upperservo": "/setServoAngle/UpperServo",
        "ussdistance": "/getDistance",
        "imagecapture": "/captureImage"
      }
    }
  }
}
```

## Programs

application1 consist of:

- application1.py
- visualize_1.py
- visualize_2.py
- config.schema.json (schema file)

*Pre-requsites*

install required dependencies using pip and requirements.txt

**Note**: preferred to have python virtual environment

```bash
pip install -r requirements.txt
```

----

**application1.py**

* application1.py is the main program for this application
* application1 is also called as 180_180_dome_application
* It can capture distance using ultrasonic sensor and/or camera image of the top dome view of the robot
* based on configurations, the extent of dome will be captured

Run the program using python:

```bash
python application1.py
```

Once the program completes, the data will be saved in datadir folder.

----

**visualize_1.py**

* visualize_1.py is basic level of visualizing colelcted data.
* Provides only 2D visualization
* use *visualize_2.py* for improved visualization

**visualize_2.py**

* visualize_2.py is enhanced visualization over visualize_1.py
* Provides scatter of all angles collected distance data
* Provides 2d scatter dump of all angles collected distance data
* Provides identified environment boundaries (of level of robot)

run the visualize_2.py with python:

```bash
python visualize_2.py
# Note: visualize_2.py uses the same config file of application1.py
```


## Data

**Note** that both datadir and stitched data will be cleared off when you re-run your program.

* datadir will be cleared if clean_data_dir_always is true in config.json
* stitched data will be cleared everytime you run any visualize program

Make sure to backup data if necessary.


*collected data*

- Data collected / captured will be stored in datadir (or whatever folder name configured in config.json)
- json file consist of timestamp, postion, angle (for which it is configured), distance data, image frame data. json file names will be in format verticleangle_horizontalangle.json
- image frames (if camera module enabled). Two files will be saved, one with filename format of verticleangle_horizontalangle.png and other equivalent uuid.png

----

*stitched data*

- heatmap.png a heatmap data based on ultrasonic distance data
- plotted.png is predicted environment boundaries based on scanned data
- cammap.png (if camera module is enabled) stitched frames of all angles data collected


## Hardware

- requires one base servo (horizontal sweep)
- optionally (but preferred) upper servo (verticle sweep)
- ultrasonic sensor mounted on base or upperservo to getdistance
- optionally mount camera module for capturing images

Refer Medha 2.0 documentation hardware section for more information