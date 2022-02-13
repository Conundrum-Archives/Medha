import os
import shutil
import cv2
import sys
import json
import time
import atexit
import pyfiglet
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# import warnings
# warnings.simplefilter("ignore", DeprecationWarning)

sys.path.append('../')
from Utils.Config import get_app_config
from Utils.LogModule import init_logger
from Utils.application1_util1 import rotate_image, create_solid_color_image, write_text_on_image, obst_range_color, data_uri_to_cv2_img, quadrant_modding, get_point_in_angle_vh, telemetry_collections_v1

log = init_logger()

# initialize labels
APPLICATION_ID = "application1"
APPLICATION_NAME = "Dome_Top_180x180 Visualizer 2"

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
log.info("data directory is set to: {datadir}\n\nNot correct? terminate this program and check configurations\n\n".format(datadir=data_dir))

if (os.path.exists(stitchdir)):
  log.warning("Clearing datadir: {datadir}".format(datadir=stitchdir))
  shutil.rmtree(stitchdir)

os.makedirs(stitchdir, exist_ok=True)


tc_v1 = telemetry_collections_v1(APPLICATION_ID)
tc_v1.visualize_2_loop_estimate()
time.sleep(10)

tc_v1.timer_1("fullprogram", "start")



start_angle_h=config["scan_config"]["baseservo_start_angle"]
start_angle_v=config["scan_config"]["upperservo_start_angle"]
steph = config["scan_config"]["baseservo_sampling"]
stepv = config["scan_config"]["upperservo_sampling"]
extenth = config["operating_device"]["modules"]["baseservo"]["max_angle"]
extentv = config["operating_device"]["modules"]["upperservo"]["max_angle"]
rotate = 0
enable360 = True

mapcoordinates = {
  "x": [],
  "y": [],
  "z":[]
}

tc_v1.timer_1("mapping-coordinated", "start")

heatmap_images_h = []
cam_images_h = []

for h in range(start_angle_h, extenth+steph, steph):
  heatmap_images_v = []
  cam_images_v = []



  for v in range(start_angle_v, extentv+int(stepv/2), stepv):
    angle = str(v) + "_" + str(h)
    log.info("ANGLE: {}".format(angle))
    with open(os.path.join(data_dir, angle + ".json"), "r") as dfile:
      tc_v1.samples_processed_count("samples")
      angledata = json.loads(dfile.read())
      img = create_solid_color_image(height=616, width=820, rgb_color=obst_range_color(angledata["data"]["distance"]))
      img = write_text_on_image(img, str("v" + str(v) + ":h" + str(h) + "\n[" + str(angledata["data"]["distance"]) + "]"))
      heatmap_images_v.append(img)

      # read base64 image file
      if (config["operating_device"]["modules"]["camera"]["enabled"]):
        with open(os.path.join(data_dir, angledata["data"]["imageFrame"]), "rb") as cfile:
          cam_images_v.append(rotate_image(data_uri_to_cv2_img(cfile.read()), rotate))

      modder = quadrant_modding(h, v)
      mapcoordinates["x"].append(get_point_in_angle_vh(h, v, angledata["data"]["distance"], "x"))
      mapcoordinates["y"].append(get_point_in_angle_vh(h, v, angledata["data"]["distance"], "y"))
      mapcoordinates["z"].append(get_point_in_angle_vh(h, v, angledata["data"]["distance"], "z"))
      log.debug("Distance value: {}".format(angledata["data"]["distance"]))
      log.debug("modder in upper quadrants: {}".format(modder))
      log.debug("coordinates: x={x}, y={y}, z={z}".format(x=mapcoordinates["x"][-1], y=mapcoordinates["y"][-1], z=mapcoordinates["z"][-1]))


  heatmap_images_h.append(np.concatenate(heatmap_images_v[::-1], axis=0))

  if (config["operating_device"]["modules"]["camera"]["enabled"]):
    cam_images_h.append(np.concatenate(cam_images_v[::-1], axis=0))



if (enable360):
  for h in range(180 - start_angle_h, 180 - start_angle_h + steph, steph):
    heatmap_images_v = []


    for v in range(start_angle_v, extentv+int(stepv/2), stepv):
      angle = str(v) + "_" + str(h)
      log.info("ANGLE: {}".format(angle))
      with open(os.path.join(data_dir, angle + ".json"), "r") as dfile:
        angledata = json.loads(dfile.read())
        img = create_solid_color_image(height=616, width=820, rgb_color=obst_range_color(angledata["data"]["distance"]))
        img = write_text_on_image(img, str("v" + str(v) + ":h" + str(h) + "\n[" + str(angledata["data"]["distance"]) + "]"))
        heatmap_images_v.append(img)
        modder = quadrant_modding(h, v)
        mapcoordinates["x"].append(get_point_in_angle_vh(h, v, angledata["data"]["distance"], "x") * modder["x"])
        mapcoordinates["y"].append(get_point_in_angle_vh(h, v, angledata["data"]["distance"], "y") * modder["y"])
        mapcoordinates["z"].append(get_point_in_angle_vh(h, v, angledata["data"]["distance"], "z") * modder["z"])
        log.debug("Distance value: {}".format(angledata["data"]["distance"]))
        log.debug("modder in lower quadrants: {}".format(modder))
        log.debug("coordiantes: x={x}, y={y}, z={z}".format(x=mapcoordinates["x"][-1], y=mapcoordinates["y"][-1], z=mapcoordinates["z"][-1]))
        
    heatmap_images_h.append(np.concatenate(heatmap_images_v[::-1], axis=0))

tc_v1.timer_1("mapping-coordinated", "stop")

#################### 3D ###########################################################
fig = plt.figure("3d Representation")
ax = plt.axes(projection='3d')

ax.set_xlabel('$X$', fontsize=20)
ax.set_ylabel('$Y$', fontsize=20)

ax.scatter(mapcoordinates["x"], mapcoordinates["y"], mapcoordinates["z"])
###################################################################################


#################### 2D ###########################################################
fig = plt.figure("2d Representation")
plt.scatter(mapcoordinates["x"], mapcoordinates["y"])
# plot origin point
plt.scatter([0], [0], color="red")
###################################################################################


#################### 2D - boundary 1 ##############################################
fig = plt.figure("2d boundary Representation")

# plot origin / where robot is located
plt.plot(0,0,'ro')

dist_arr = {
  "px": 0,
  "nx": 0,
  "py": 0,
  "ny": 0
}

# plot x = dist
if os.path.exists(os.path.join(data_dir, "0_0.json")):
  with open(os.path.join(data_dir, "0_0.json"), "r") as ddata:
    dist_arr["px"] = json.loads(ddata.read())["data"]["distance"]
    log.info("Right: {}".format(dist_arr["px"]))
  x = np.full((1000), dist_arr["px"])
  y = np.linspace(-600, 600, 1000)
  plt.scatter(x, y, s=3)
  plt.text(np.median(x) + 10, np.median(y), "right")

# plot other side of x
if os.path.exists(os.path.join(data_dir, "0_180.json")):
  with open(os.path.join(data_dir, "180_0.json"), "r") as ddata:
    dist_arr["nx"] = json.loads(ddata.read())["data"]["distance"]
    log.info("Left: {}".format(dist_arr["nx"]))
  x = np.full((1000), dist_arr["nx"] * -1)
  y = np.linspace(-600, 600, 1000)
  plt.scatter(x, y, s=3)
  plt.text(np.median(x) - 20, np.median(y), "left")

# plot y = dist
if os.path.exists(os.path.join(data_dir, "0_90.json")):
  with open(os.path.join(data_dir, "0_90.json"), "r") as ddata:
    dist_arr["py"] = json.loads(ddata.read())["data"]["distance"]
    log.info("Front: {}".format(dist_arr["py"]))
  y = np.full((1000), dist_arr["py"])
  x = np.linspace(-600, 600, 1000)
  plt.scatter(x, y, s=3)
  plt.text(np.median(x), np.median(y) + 20, "front")

# plot other side of y
if os.path.exists(os.path.join(data_dir, "180_90.json")):
  with open(os.path.join(data_dir, "180_90.json"), "r") as ddata:
    dist_arr["ny"] = json.loads(ddata.read())["data"]["distance"]
    log.info("Back: {}".format(dist_arr["ny"]))
  y = np.full((1000), dist_arr["ny"] * -1)
  x = np.linspace(-600, 600, 1000)
  plt.scatter(x, y, s=3)
  plt.text(np.median(x), np.median(y) - 30, "back")

###################################################################################


# UNCOMMENT LATER WHEN NEEDED

log.debug("heatmap final stitch")
heatmap_images_final = np.concatenate(heatmap_images_h[::-1], axis=1)

if (config["operating_device"]["modules"]["camera"]["enabled"]):
  log.debug("cammap final stitch")
  cam_images_final = np.concatenate(cam_images_h[::-1], axis=1)

log.debug("saving heatmap")
cv2.imwrite(os.path.join(stitchdir, "heatmap.png"), heatmap_images_final)

if (config["operating_device"]["modules"]["camera"]["enabled"]):
  log.debug("saving cammap")
  cv2.imwrite(os.path.join(stitchdir, "cammap.png"), cam_images_final)

log.debug("saving plotted")
plt.savefig(os.path.join(stitchdir, "plotted.png"))

# print telemetry data
tc_v1.timer_1("fullprogram", "stop")
tc_v1.print_times()

log.info("Opening plotted window . . .")
plt.show()