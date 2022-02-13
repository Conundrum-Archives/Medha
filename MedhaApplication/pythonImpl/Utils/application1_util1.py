
import cv2
import math
import base64
import requests
import datetime
import numpy as np
from prettytable import PrettyTable
from Utils.Config import get_app_config
from Utils.LogModule import init_logger

# initialize logger
log = init_logger()

# medthod to get point coordinated for an angle captured - for mapping on visualizer
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

# method to get point coordinated in 3d plane
def get_point_in_angle_vh(h_angle, v_angle, dist, mode="x"):
  if (mode == "x"):
    # use cos
    angle_in_rad = (h_angle*math.pi)/180
    x = dist * math.cos(angle_in_rad)
    return x
  elif (mode == "y"):
    # use sin
    angle_in_rad = (h_angle*math.pi)/180
    y = dist * math.sin(angle_in_rad)
    return y
  elif (mode == "z"):
    # use sin in yz plane
    angle_in_rad = (v_angle*math.pi)/180
    z = dist * math.sin(angle_in_rad)
    return z

# method to rotate image with angle value in degrees
def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

# method to color heatmap frames
def obst_range_color(dist):
  if (type(dist) != float):
    raise ValueError("angle must be float. Supplied:" + str(dist))
  rng = {
    "near": {"min": 0, "max": 50, "color": (255,0,0)},
    "mid": {"min": 50, "max": 100, "color": (255,255,0)},
    "far": {"min": 100, "max": 99999, "color": (0,255,0)}
  }
  
  for r in rng:
    if ( (dist >= rng[r]["min"]) and (dist < rng[r]["max"])):
      return rng[r]["color"]
  return (255,255,255)



# get quadrant modding for mapping on visualizer in 180-180 mirror flip
def quadrant_modding(h, v):
  # z is always positive (upper dome)
  # h 0-90 v 0-90 x:+ y:+
  # h 90-180 v 0-90 x:- y:+
  # h 0-90 v 90-180 x:- y:-
  # h 90-180 v 90-180 x:+ y:-
  mod = {"x":1, "y":-1, "z":1}
  if (h>=180 and h<270):
    mod["x"] = -1
  return mod

# create solid color image (for background)
def create_solid_color_image(height=300, width=300, rgb_color=(255,255,255)):
  # create black color image
  image = np.zeros((height, width, 3), np.uint8)
  
  # opencv uses bgr, we must convert
  color = tuple(reversed(rgb_color))
  
  # fill required color
  image[:] = color
  
  return image

# write text on image
def write_text_on_image(image, text):
  height, width, channels = image.shape
  return cv2.putText(image,str(text), (int(width/3), int(height/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

# utility module to convert data_uri image to cv2 image
def data_uri_to_cv2_img(encoded_data):
  nparr = np.fromstring(base64.b64decode(base64.b64encode(encoded_data).decode('ascii')), np.uint8)
  img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
  return img


# telemetry class for measuring time and other metrics
class telemetry_collections_v1:

  def __init__(self, app_id="application1"):
    self.config = get_app_config(app_id)
    self.timer = {}
    self.prtable = PrettyTable()
    self.samples_processed_count_var = {}

  def visualize_2_loop_estimate(self):
    total_time = 25  # in milli sec

    if (self.config["operating_device"]["modules"]["camera"]["enabled"]):
      total_time = total_time + 10

    baseloops = round(self.config["operating_device"]["modules"]["baseservo"]["max_angle"] / self.config["scan_config"]["baseservo_sampling"]) + 1
    upperloops = round(self.config["operating_device"]["modules"]["upperservo"]["max_angle"] / self.config["scan_config"]["upperservo_sampling"]) + 1

    self.total_time_predicted = (baseloops * upperloops * total_time)/1000
    log.info("The program takes minimum {time} seconds to complete\n".format(time=self.total_time_predicted))

  def timer_1(self, name="temp", mode="start"):
    if (mode == "start"):
      self.timer[name] = {}
      self.timer[name]["start_time"] = datetime.datetime.now()
      return self.timer[name]["start_time"]
    elif (mode == "stop"):
      self.timer[name]["stop_time"] = datetime.datetime.now()
      self.timer[name]["total_time"] = self.timer[name]['stop_time'] - self.timer[name]["start_time"]
      return (self.timer[name]["stop_time"] - self.timer[name]["start_time"]).microseconds
    elif (mode == "getall"):
      return self.timer

  def samples_processed_count(self, name="default"):
    if (name not in self.samples_processed_count_var):
      self.samples_processed_count_var[name] = 0
    self.samples_processed_count_var[name] = self.samples_processed_count_var[name] + 1

  def print_times(self):
    self.prtable.field_names = ["program", "timetaken"]
    alltimes = self.timer_1(mode="getall")
    self.prtable.add_row(["total time predicted", self.total_time_predicted*1000])
    for timename in alltimes:
      self.prtable.add_row([timename, (alltimes[timename]["total_time"]).microseconds/1000])

    # add samples count
    self.prtable.add_row(["total samples processed", self.samples_processed_count_var["samples"]])
    log.debug("telemetry data:\n{tdata}".format(tdata=self.prtable))


# request wrapper class to handle API
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