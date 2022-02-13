import os
import cv2
import base64
import numpy as np

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

def get_image_base64(image):
  cv2.imwrite("test.png", image)
  base64data = str(base64.b64encode(open("test.png", "rb").read()).decode("ascii"))
  if (os.path.exists("test.png")):
    os.unlink("test.png")
  return base64data