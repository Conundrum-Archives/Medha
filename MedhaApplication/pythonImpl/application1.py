# -*- coding: utf-8 -*-
"""
Created on Sat Feb  12 21:08:40 2022

@author: NikhilTanni
"""

import os
import sys
import json
import time
import uuid
import atexit
import base64
import msvcrt
import shutil
import pyfiglet
import requests
import numpy as np
import matplotlib.pyplot as plt
from Utils.Config import get_app_config
from Utils.LogModule import init_logger
from Utils.application1_util1 import request_handler
from Utils.application1_util1 import get_point_in_angle

# initialize logger
log = init_logger()

# initialize labels
APPLICATION_ID = "application1"
APPLICATION_NAME = "Dome_Top_180x180"

# logo and app branding
try:
  f = pyfiglet.Figlet(font='banner3-D')
  print(f.renderText(" MEDHA "))
except:
  log.warning("MEDHA")

# exit handler
def exit_handler():
  log.info("Program: {appname} is exiting now\n\n{appname} message: See you soon untill then good bye!!".format(appname=APPLICATION_NAME))
atexit.register(exit_handler)

# read config
config = get_app_config(APPLICATION_ID)

data_dir = config["data_dir"] if "data_dir" in config else "datadir_default"


log.info("starting application: {appname} [ID:{appid}]".format(appname=APPLICATION_NAME, appid=APPLICATION_ID))
log.info("data directory is set to: {datadir}".format(datadir=data_dir))

# setup / clean data directory to save run-time data
if (os.path.exists(data_dir)):
  if (("clean_data_dir_always" in config) and (config["clean_data_dir_always"])):
    log.warning("Clearing datadir: {datadir}".format(datadir=data_dir))
    shutil.rmtree(data_dir)
  else:
    data_dir = data_dir + str(time.strftime("%Y%m%d-%H%M%S"))
    log.warning("creating timestamped data_dir: {newdatadir}".format(newdatadir=data_dir))
    
os.makedirs(data_dir, exist_ok=True)


# check device config
DEVICE_BASEURL = config["operating_device"]["base_url"] if (("operating_device" in config) and ("base_url" in config["operating_device"])) else "http://localhost:5000"
log.debug("\n\nOPERATING DEVICE BASE URL: {device_url}.\n\nNot correct? terminate this program and check configurations\n\n".format(device_url=DEVICE_BASEURL))
time.sleep(10)

# check if base url reachable
req_handler = None
try:
  req_handler = request_handler(APPLICATION_ID)
except Exception as e:
  log.error("Something went wrong while checking base_url. Check if controller on device in running and same host:port is configured in this configurations")
  sys.exit(0)

log.info("starting {appname}".format(appname=APPLICATION_NAME))

proceedAlways = config["scan_config"]["proceed_always"]
if (proceedAlways):
  log.warning("proceedAlways is enabled. The program will continue without askin for confirmation")
else:
  log.info("proceedAlways is disabled. The program will ask for confirmaton before continuing")


start_angle_h=config["scan_config"]["baseservo_start_angle"]
start_angle_v=config["scan_config"]["upperservo_start_angle"]
steph = config["scan_config"]["baseservo_sampling"]
stepv = config["scan_config"]["upperservo_sampling"]
extenth = config["operating_device"]["modules"]["baseservo"]["max_angle"]
extentv = config["operating_device"]["modules"]["upperservo"]["max_angle"]

# check is start angle is less than min_angle
if (start_angle_h < config["operating_device"]["modules"]["baseservo"]["min_angle"]):
  raise ValueError("baseservo_start_angle cannot be less than minimum angle of baseservo")
if (start_angle_v < config["operating_device"]["modules"]["upperservo"]["min_angle"]):
  raise ValueError("upperservo_start_angle cannot be less than minimum angle of upperservo")


# define visualizer
plt.title("Scan Visualizaton")
plt.interactive(True)
plt.grid()


for h in range(start_angle_h, extenth+steph, steph):
  proceed_flag1 = b"r"
  angleresp2 = {}
  uid = uuid.uuid4().hex
  
  while(proceed_flag1.decode() == "r"):
    angleresp2 = req_handler.set_baseservo_angle(h)
    if (not proceedAlways):
      log.debug("Base angle={h}.\nPress r to retry. any other key to proceed next".format(h=str(h)))
      proceed_flag1 = msvcrt.getch()
    else:
      time.sleep(1)
      break

  for v in range(start_angle_v, extentv+int(stepv/2), stepv):

    proceed_flag1 = b"r"
    angleresp = {}

    while(proceed_flag1.decode() == "r"):
      angleresp = req_handler.set_upperservo_angle(v)
      if (not proceedAlways):
        log.debug("Upper angle={v}.\nPress r to retry. any other key to proceed next".format(v=str(v)))
        proceed_flag1 = msvcrt.getch()
      else:
        time.sleep(1)
        break

    log.info("Angle set to: base={h}, upper={v}".format(h=str(h), v=str(v)))

    proceed_flag1 = b"r"
    dist = 0

    while(proceed_flag1.decode() == "r"):
      dist = req_handler.get_distance()
      if (not proceedAlways):
        log.debug("Got distance={d}\nPress r to retry. any other key to proceed next".format(d=str(dist)))
        proceed_flag1 = msvcrt.getch()
      else:
        break
    log.info("Captured Distance: {d}".format(d=str(dist)))

    if (config["operating_device"]["modules"]["camera"]["enabled"] if "camera" in config["operating_device"]["modules"] else False):
      log.info("capturing image: do not shake device as it may cause unclear image")
      img = req_handler.get_capture()

      log.debug("saving image for " + str(v) + "_" + str(h))
      with open(os.path.join(data_dir, str(v) + "_" + str(h) + ".png"), "wb") as fh:
        fh.write(base64.b64decode(img["data"]["base64"]))

      with open(os.path.join(data_dir, uid + ".png"), "wb") as ft:
        ft.write(base64.b64decode(img["data"]["base64"]))

    # write data to file
    with open(os.path.join(data_dir, str(v) + "_" + str(h) + ".json"), "w") as fd:
      jsdata = {
        "timestamp": "",
        "position": "",
        "angle": {
          "h": h,
          "v": v
        },
        "data": {
          "distance": dist["data"]["distance"],
          "imageFrame": uid + ".png",
          "imageFrameAngled": str(v) + "_" + str(h) + ".png"
        }
      }
      json.dump(jsdata, fd, ensure_ascii=False, indent=4)
    
    log.debug("mapping the collected data to VISUALIZER")
    pt = {
      "x": get_point_in_angle(h, dist["data"]["distance"], "x"),
      "y": get_point_in_angle(h, dist["data"]["distance"], "y")
    }

    log.debug("[VISUALIZER] Angle: {angle}  |  Mapped-Distance: {mdist}".format(angle=h, mdist=dist["data"]["distance"]))

    plt.plot(pt["x"], pt["y"], 'bo')
    plt.text(pt["x"]+.05, pt["y"]+.05,  str(h)+"`", fontsize=9)
    plt.plot([0, pt["x"]], [0, pt["y"]], 'g', linestyle="--")

    # save partial data: incase program stops
    plt.savefig(os.path.join(data_dir, 'visualizer.png'), format='png', dpi=300)

    # one loop done. sleep to avoid overloading system calls
    time.sleep(1)


# reset servo position
req_handler.set_baseservo_angle(0)
req_handler.set_upperservo_angle(0)
time.sleep(2)
plt.savefig(os.path.join(data_dir, 'visualizer.png'), format='png', dpi=1200)
log.info("visualizer image saved as visualizer.png")
  
