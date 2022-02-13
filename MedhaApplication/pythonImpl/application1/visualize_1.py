import os
import cv2
import sys
import json
import atexit
import base64
import shutil
import pyfiglet
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# append parent directory for utils
sys.path.append('../')
from Utils.Config import get_app_config
from Utils.LogModule import init_logger
from Utils.application1_util1 import rotate_image, create_solid_color_image, write_text_on_image, obst_range_color, data_uri_to_cv2_img

log = init_logger()

# initialize labels
APPLICATION_ID = "application1"
APPLICATION_NAME = "Dome_Top_180x180 Visualizer 1"

# logo and app branding
try:
  f = pyfiglet.Figlet(font='banner3-D')
  print(f.renderText(" MEDHA "))
except Exception as e:
  log.warning("MEDHA")

# exit handler
def exit_handler():
  log.info("Program: {appname} is exiting now\n\n{appname} message: See you soon untill then good bye!!".format(appname=APPLICATION_NAME))
atexit.register(exit_handler)

# read config
config = get_app_config(APPLICATION_ID)

data_dir = config["data_dir"] if "data_dir" in config else "datadir_default"
stitchdir = "stitchdata"


log.info("starting application: {appname} [ID:{appid}]".format(appname=APPLICATION_NAME, appid=APPLICATION_ID))
log.info("data directory is set to: {datadir}".format(datadir=data_dir))

if (os.path.exists(stitchdir)):
  log.warning("Clearing datadir: {datadir}".format(datadir=stitchdir))
  shutil.rmtree(stitchdir)

os.makedirs(stitchdir, exist_ok=True)



start_angle_h=config["scan_config"]["baseservo_start_angle"]
start_angle_v=config["scan_config"]["upperservo_start_angle"]
steph = config["scan_config"]["baseservo_sampling"]
stepv = config["scan_config"]["upperservo_sampling"]
extenth = config["operating_device"]["modules"]["baseservo"]["max_angle"]
extentv = config["operating_device"]["modules"]["upperservo"]["max_angle"]
rotate = 0

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlabel('$X$', fontsize=20)
ax.set_ylabel('$Y$', fontsize=20)


heatmap_images_v = []
cam_images_v = []
for v in range(start_angle_v, extentv+stepv, stepv):
  heatmap_images_h = []
  cam_images_h = []
  for h in range(start_angle_h, extenth+int(steph/2), steph):
    angle = str(v) + "_" + str(h)
    log.debug("ANGLE: {}".format(angle))
    with open(os.path.join(data_dir, angle + ".json"), "r") as dfile:
      angledata = json.loads(dfile.read())
      img = create_solid_color_image(height=616, width=820, rgb_color=obst_range_color(angledata["data"]["distance"]))
      img = write_text_on_image(img, str("v" + str(v) + ":h" + str(h) + "\n[" + str(angledata["data"]["distance"]) + "]"))
      heatmap_images_h.append(img)
      
      # read base64 image file
      if (config["operating_device"]["modules"]["camera"]["enabled"]):
        with open(os.path.join(data_dir, angledata["data"]["imageFrame"]), "rb") as cfile:
          cam_images_h.append(rotate_image(data_uri_to_cv2_img(cfile.read()), rotate))
  heatmap_images_v.append(np.concatenate(heatmap_images_h[::-1], axis=1))

  if (config["operating_device"]["modules"]["camera"]["enabled"]):
    cam_images_v.append(np.concatenate(cam_images_h[::-1], axis=1))


  
log.debug("heatmap final stitch")
heatmap_images_final = np.concatenate(heatmap_images_v[::-1], axis=0)

if (config["operating_device"]["modules"]["camera"]["enabled"]):
  log.debug("cammap final stitch")
  cam_images_final = np.concatenate(cam_images_v[::-1], axis=0)


log.debug("saving heatmap")
cv2.imwrite(os.path.join(stitchdir, "heatmap.png"), heatmap_images_final)

if (config["operating_device"]["modules"]["camera"]["enabled"]):
  log.debug("saving cammap")
  cv2.imwrite(os.path.join(stitchdir, "cammap.png"), cam_images_final)