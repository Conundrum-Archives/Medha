import base64
from picamera import PiCamera

class CameraModule:

  """
  CameraModule class interfaces camera component and includes:
  - functionality to capture with specifications
  - get base64 format of the image
  """

  def __init__(self, resolution="MAX", rotate=0, capturefile="capture.jpg"):
    self.camera = PiCamera()

    # check for resolution
    if (resolution == "MAX"):
      self.camera.resolution = self.camera.MAX_RESOLUTION
    elif (type(resolution) is tuple):
      self.camera.resolution = resolution
    else:
      raise ValueError("invalid resolution value supplied. expecting MAX or tuple of (width, height) value in pixels")

    # check for rotate value
    if (type(rotate) is not int):
      raise ValueError("value of rotate must be int")
    elif(rotate < 0 or rotate > 360):
      raise ValueError("value of rotate must be between 0 and 360")
    else:
      self.camera.rotation = rotate

    # check for capturefile
    if((type(capturefile) is not str)):
      raise ValueError("check the value of capturefile")
    elif(not capturefile.endswith(".jpg") and not capturefile.endswith(".png")):
      raise ValueError("capturefile extension must be either .png or .jpg")
    else:
      self.capturefile = capturefile

  # method to capture from camera
  def capture(self, capturefile=None):
    if(capturefile is None):
      capturefile = self.capturefile
    
    self.camera.capture(capturefile)

  # method to get base64 form of the captured image
  def get_base64_image(self):
    return str(base64.b64encode(open(self.capturefile,"rb").read()).decode("ascii"))

  # method to close and cleanup camera resource
  def cleanup(self):
    self.camera.close()