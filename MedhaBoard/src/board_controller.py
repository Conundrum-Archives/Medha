import gc
import os
import signal
import atexit
from flask import Flask, request
from Utils.Config import get_config
from Utils.RespUtils import format_response
import medhalib.Utils.LogModules as LogModule
from medhalib.Actuators.Servo import Servo180
from medhalib.Sensors.Image import CameraModule
from medhalib.Sensors.Sound import UltraSonicSensor

# read configuration
config = get_config()

# check debug
if (config['server']['devdebug']):
  os.environ["DEBUGMODE"] = "true"

# initialize logger
log = LogModule.init_logger()

# initialize app
app = Flask(__name__)

# initialize pins
ultrasonicsensor_trig_pin = config["board_bcmpin"]["ultrasonicsensor_trig"]
ultrasonicsensor_echo_pin = config["board_bcmpin"]["ultrasonicsensor_echo"]
baseservo_pin = config["board_bcmpin"]["baseservo"]
upperservo_pin = config["board_bcmpin"]["upperservo"]

# initialize methods
uss_sensor_1 = UltraSonicSensor(ultrasonicsensor_trig_pin, ultrasonicsensor_echo_pin)
base_servo = Servo180(baseservo_pin)
upper_servo = Servo180(upperservo_pin)

content_type = 'application/json'

# registed at exit cleanup
def cleanup():
  uss_sensor_1.cleanup()
  base_servo.cleanup()
  upper_servo.cleanup()

atexit.register(cleanup)
signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)


# endpoint to get distance from ultrasonic sensor
@app.route('/get_distance')
def get_distance():
  resp_data = {"status":200,"message":"","data":{}}

  try:
    resp_data["data"]["distance"] = uss_sensor_1.get_distance()
  except Exception as e:
    resp_data["status"] = 500
    resp_data["message"] = "Error while getting distance from USSensor:"
    resp_data["error"] = str(e)

  return format_response(resp_data), resp_data["status"], {'ContentType':content_type}

# endpoint to set servo position : expects path-query parameter: servoname=BaseServo, UpperServo and query parameter: angle=range(0,180)
@app.route('/set_servo_angle/<servoname>')
def set_servo_angle( servoname):
  servo_list = ["BaseServo", "UpperServo"]

  resp_data = {"status":200,"message":"","data":{}}
  angle = int(request.args.get("angle"))
  if (servoname not in servo_list):
    resp_data["status"] = 400
    resp_data["message"] = "Invalid Servo name provided"
    resp_data["data"]["available"] = servo_list
  elif (angle < 0):
    resp_data["status"] = 400
    resp_data["message"] = "angle valud cannot be less than 0"
  elif (angle > 180):
    resp_data["status"] = 400
    resp_data["message"] = "angle valud cannot be greater than 180"
  else:
    resp_data["status"] = 200
    resp_data["message"] = "Base servo set to angle: " + str(angle)
    if (servoname == "BaseServo"):
      base_servo.set_servo_angle(int(angle))
    elif (servoname == "UpperServo"):
      upper_servo.set_servo_angle(int(angle))

  return format_response(resp_data), resp_data["status"], {'ContentType':content_type}

# endpoint to capture image from camera module
@app.route('/capture_image')
def capture_image():
  resp_data = {"status":200,"message":"","data":{}}
  flag = False

  cam_settings = {
    "resolution": "MAX",
    "rotate": int(request.args.get("rotate")) if request.args.get("rotate") is not None else 0,
    "captureFile": str(request.args.get("captureFile")) if request.args.get("captureFile") is not None else "capture.jpg"
  }

  if (request.args.get("resWidth") is not None and request.args.get("resHeight") is not None):
    resW = request.args.get("resWidth")
    resH = request.args.get("resHeight")
    try:
      if (str(resW) == "MAX" and str(resH) == "MAX"):
        cam_settings["resolution"] = "MAX"
      else:
        resW = int(resW)
        resH = int(resH)
        if(resW <= 100 or resH <= 100):
          raise ValueError("resolution value must be greater than 100")
        else:
          cam_settings["resolution"] = (resW, resH)
      flag = True
    except Exception as e:
      resp_data["status"] = 400
      resp_data["message"] = "invalid resWidth or resHeight provided. Accepted MAX or number value greater than 100"
      resp_data["data"]["error"] = str(e)
      flag = False
    del resW
    del resH
    gc.collect()

    try:
      if (flag):
        camera = CameraModule(resolution=cam_settings["resolution"], rotate=cam_settings["rotate"], capturefile=cam_settings["captureFile"])
        resp_data["data"]["cam_settings"] = cam_settings

        # cleanup
        del cam_settings
        gc.collect()

        camera.capture()

        if (request.args.get("getbase64") is not None and str(request.args.get("getbase64")).lower() == "true"):
          resp_data["data"]["base64"] = camera.getBase64()


        camera.cleanup()
        del camera
        gc.collect()

        resp_data["status"] = 201
        resp_data["message"] = "image captured successfully"
        

    except Exception as e:
      resp_data["status"] = 500
      resp_data["message"] = "Error occured while capturing image"
      resp_data["data"]["error"] = str(e)
    finally:
      gc.collect()
      
    return format_response(resp_data), resp_data["status"], {'ContentType':content_type}

# home end point for default api path
@app.route('/')
def home():
  resp_data = {"status":200,"message":"","data":{}}
  resp_data['message'] = "this is home API"
  return format_response(resp_data), resp_data["status"], {'ContentType':content_type}

port = int(os.environ.get("PORT", config['server']['port']))
log.info("starting server at port {port}".format(port=port))
app.run(host='0.0.0.0',port=port,debug=config['server']['serverdebug'])
