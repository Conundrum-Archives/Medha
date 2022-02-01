
# Conundrum-Archives/Project-Medha


Project-Medha is a codebase for Medha library and on-board snapshot. You can use use the medhalibrary by building from scratch or directly install from pip.

This repo consist of two components:

- MedhaLibrary: consit of library and classes to interface sensors, actuators and other on-board functionalities
- MedhaBoard: consist of implementation from MedhaLibrary. also reffered to as board-controller.

---

[![GitHub license](https://img.shields.io/github/license/Conundrum-Archives/Medha-Rover)](https://github.com/Conundrum-Archives/Medha-Rover/blob/release/2.0/LICENSE)

![GitHub repo size](https://img.shields.io/github/repo-size/Conundrum-Archives/Medha-Rover)

![GitHub last commit](https://img.shields.io/github/last-commit/Conundrum-Archives/Medha-Rover)

## Usage

### Development setup

seting up the repo for local development:

- clone the repo or download the zip from github
```bash
git clone https://github.com/Conundrum-Archives/Medha.git --branch release/2.0
```
- create a virtual environment
```bash
cd Medha
python -m venv venv
venv\Scripts\activate      #Windows
source venv/bin/activate   #Linux
```
- Install dependencies using pip
```bash
pip install -r requirements/requirements_board_dev.txt
```
- Now codebase is ready for local development. After this either you can run MedhaBoard or develop and build MedhaLibrary


### Building MedhaLibrary

- Make changes inside MedhaLibrary folder (if not skip this step)
- Run the build command to create distributable pypi package
```bash
python setup.py sdist
```
- Run the tests (optional)
```bash
python setup.py test
```
- Navigate to dist directory. There you will get a tar.gz file which is a pypi package


### Running MedhaBoard

- Configure config.py with appropiate values for port, debugmodes.
- Make sure modules are installed using pip command
```bash
pip install -r requirements/requirements_board_dev.txt  #if local dev

pip install -r requirements/requirements_board_dep.txt  #if actual deployment
```
- Make sure to install the MedhaLibrary either from pypi or local build created in previous setup (Building MedhaLibrary)
```bash
pip install /path/to/dist/MedhaLibrary-2.0x.y.x.tar.gz  #replace x.y.z with actual file name

pip install MedhaLibrary  #to install from pypi
```
- Run the python file
```bash
python board_controller.py
```




## Deployment

To deploy this project on actual board...

- Clone this repo or download release package from github to raspberry pi board
```bash
git clone https://github.com/Conundrum-Archives/Medha.git --branch release/2.0
```

- Install dependencies using pip
```bash
pip install -r requirements/requirements_board_dep.txt

# note: use virtual env if you have setup
```

- Configure config.py with appropiate values or leave default
- Run board_controller.py
```bash
python board_controller.py
```

Note: You may need to expose port for which the controller is listening. Check your config.json for port number.

## MedhaBoard Endpoints

The list of MedhaBoard endpoints:

---

GET: **/get_distance**

Response code: 200, 500

---

GET: **/set_servo_angle/<servoname>?angle=<anglevalue>**

servoname=BaseServo or UpperServo

query-params:
- anglevalue=0 to 180

Response code: 200, 400, 500

---

GET: **/capture_image**

query-params:
- resWidth=MAX or value greater than 100
- redHeight=MAX or vlue greater than 100
- rotate=0 to 359
- captureFile=filename.jpg or filename.png
- getbase64=true or false

Response code: 201, 400, 500


