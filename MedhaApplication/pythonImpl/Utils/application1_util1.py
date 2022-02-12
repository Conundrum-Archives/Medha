
import math
import requests
from Utils.Config import get_app_config
from Utils.LogModule import init_logger

# initialize logger
log = init_logger()


def get_point_in_angle(angle, dist, mode="x"):
  angle_in_rad = (angle*math.pi)/180
  if (mode == "x"):
    # use cos
    x = dist * math.cos(angle_in_rad)
    return x
  elif (mode == "y"):
    # use sin
    y = dist * math.sin(angle_in_rad)
    return y


class request_handler:

  def __init__(self, app_id="application1"):
    self.device_config = get_app_config(app_id)["operating_device"]
    testreq = requests.get(self.device_config["base_url"])

  # request api for device
  def set_baseservo_angle(self, angle):
    if (type(angle) != int):
      log.error("angle must be integer")
      raise Exception("angle must be integer")
    
    # validate value
    if (angle < 0 or angle > 180):
      log.error("angle must be between 0 & 180. Provided: " + str(angle))
      raise Exception("angle must be between 0 & 180. Provided: " + str(angle))
        
    # send request for angle api
    api = self.device_config["base_url"] + self.device_config["end_points"]["baseservo"]
    query_param = {"angle":angle}
    headers = {'content-type': 'application/json'}
    res = requests.get(api, params=query_param, headers=headers)
    return res.json()

  # request api for device
  def set_upperservo_angle(self, angle):
    if (type(angle) != int):
      log.error("angle must be integer")
      raise Exception("angle must be integer")
    
    # validate value
    if (angle < 0 or angle > 180):
      log.error("angle must be between 0 & 180. Provided: " + str(angle))
      raise Exception("angle must be between 0 & 180. Provided: " + str(angle))
        
    # send request for angle api
    api = self.device_config["base_url"] + self.device_config["end_points"]["upperservo"]
    query_param = {"angle":angle}
    headers = {'content-type': 'application/json'}
    res = requests.get(api, params=query_param, headers=headers)
    return res.json()

  def get_distance(self):
    # send request for angle api
    api = self.device_config["base_url"] + self.device_config["end_points"]["ussdistance"]
    headers = {'content-type': 'application/json'}
    res = requests.get(api, headers=headers)
    return res.json()

  def get_capture(self):
    # send request for angle api
    api = self.device_config["base_url"] + self.device_config["end_points"]["imagecapture"]
    headers = {'content-type': 'application/json'}
    query_param = self.device_config["modules"]["camera"]["capture_settings"]
    res = requests.get(api, headers=headers, params=query_param)
    return res.json()