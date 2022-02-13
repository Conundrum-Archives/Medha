import gc
import random
from time import sleep
from flask import Flask, request
import Utils.LogModule as LogModule
from Utils.RespUtil import resp_format
from Utils.ImageGenerator import create_solid_color_image, get_image_base64

# initialize logger
log = LogModule.init_logger()

# initialize flask app
app = Flask(__name__)

# mock handler to handle setting servo angle
@app.route('/setServoAngle/<servoname>')
def setServoAngle(servoname):
  servos_list = ["BaseServo", "UpperServo"]

  resp_data = {"status":200,"message":"","data":{}}
  angle = int(request.args.get("angle"))
  if (servoname not in servos_list):
    resp_data["status"] = 400
    resp_data["message"] = "Invalid Servo name provided"
    resp_data["data"]["available"] = servos_list
  elif (angle is None):
    resp_data["status"] = 400
    resp_data["message"] = "provide valid angle value"
  elif (angle < 0):
    resp_data["status"] = 400
    resp_data["message"] = "angle valud cannot be less than 0"
  elif (angle > 180):
    resp_data["status"] = 400
    resp_data["message"] = "angle valud cannot be greater than 180"
  else:
    resp_data["status"] = 200
    resp_data["message"] = "{servo} set to angle: {angle}".format(servo=servoname,angle=str(angle))

  return resp_format(resp_data), resp_data["status"], {'ContentType':'application/json'}

# mock handler to handle capture image
@app.route('/captureImage')
def captureImage():
  resp_data = {"status":200,"message":"","data":{}}
  flag = False

  camSettings = {
    "resolution": "MAX",
    "rotate": int(request.args.get("rotate")) if request.args.get("rotate") is not None else 0,
    "captureFile": str(request.args.get("captureFile")) if request.args.get("captureFile") is not None else "capture.jpg"
  }

  if (request.args.get("resWidth") is not None and request.args.get("resHeight") is not None):
    resW = request.args.get("resWidth")
    resH = request.args.get("resHeight")
    try:
      if (str(resW) == "MAX" and str(resH) == "MAX"):
        camSettings["resolution"] = (2592, 1944)
      else:
        resW = int(resW)
        resH = int(resH)
        if(resW <= 100 or resH <= 100):
          raise Exception("resolution value must be greater than 100")
        else:
          camSettings["resolution"] = (resW, resH)
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
        image = create_solid_color_image(height=camSettings["resolution"][1], width=camSettings["resolution"][0], rgb_color=(30,136,229))
        resp_data["data"]["camSettings"] = camSettings

        if (request.args.get("getbase64") is not None and str(request.args.get("getbase64")).lower() == "true"):
          resp_data["data"]["base64"] = get_image_base64(image)

        resp_data["status"] = 201
        resp_data["message"] = "image captured successfully"
        

    except Exception as e:
      resp_data["status"] = 500
      resp_data["message"] = "Error occured while capturing image"
      resp_data["data"]["error"] = str(e)
    finally:
      gc.collect()
      
    return resp_format(resp_data), resp_data["status"], {'ContentType':'application/json'}


# mock handler to handle get distance
@app.route('/getDistance')
def getDistance():
  resp_data = {"status":200,"message":"","data":{}}
  resp_data["data"]["distance"] = random.uniform(5, 500)

  return resp_format(resp_data), resp_data["status"], {'ContentType':'application/json'}

# home page handler
@app.route('/')
def home():
  resp_data = {"status":200,"message":"","data":{}}
  resp_data['message'] = "this is home API"
  return resp_format(resp_data), resp_data["status"], {'ContentType':'application/json'}

# start server
if __name__ == '__main__':
  log.info("starting server at port 5000")
  app.run(host='0.0.0.0', port=5000, debug=True)
