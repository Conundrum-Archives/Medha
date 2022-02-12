import os
import sys
import unittest
from unittest.mock import MagicMock, Mock


class TestSensors(unittest.TestCase):

  """TEST Sensor class and methods"""

  def test_UltraSonicSensor_get_distance(self):
    sys.modules['RPi'] =  MagicMock()
    import src.medhalib.Sensors.Sound as Sound
    self.assertEqual(Sound.UltraSonicSensor(2,3).get_distance(), 0.0)

  def test_UltraSonicSensor_cleanup(self):
    sys.modules['RPi'] =  MagicMock()
    import src.medhalib.Sensors.Sound as Sound
    try:
      Sound.UltraSonicSensor(2,3).cleanup()
    except Exception as e:
      self.fail("UltraSonicSensor cleanup failed: {}".format(e))

  def test_CameraModule_init(self):
    sys.modules['picamera'] = Mock()
    import src.medhalib.Sensors.Image as Image

    # test for exception raiser for resolution parameter: None and ""
    with self.assertRaises(ValueError) as ver:
      Image.CameraModule(None, 0, "")
    with self.assertRaises(ValueError) as ver:
      Image.CameraModule("", 0, "")

    # test for exception raiser for rotate parameter: None and ""::less than 0 and greater than 180
    with self.assertRaises(ValueError) as ver:
      Image.CameraModule("MAX", None, "")
    with self.assertRaises(ValueError) as ver:
      Image.CameraModule("MAX", "", "")
    with self.assertRaises(ValueError) as ver:
      Image.CameraModule("MAX", -1, "")
    with self.assertRaises(ValueError) as ver:
      Image.CameraModule("MAX", 361, "")

    # test for exception raiser for filename parameter: None and ""::less than 0 and greater than 180
    with self.assertRaises(ValueError) as ver:
      Image.CameraModule("MAX", 0, None)
    with self.assertRaises(ValueError) as ver:
      Image.CameraModule("MAX", 0, "test.jpgg")
    with self.assertRaises(ValueError) as ver:
      Image.CameraModule("MAX", 0, "test.pngg")

    # test for no exceptions
    Image.CameraModule("MAX", 0, "test.jpg")
    Image.CameraModule((640, 480), 0, "test.jpg")
    Image.CameraModule("MAX", 0, "test.png")

  def test_CameraModules_capture(self):
    sys.modules['picamera'] = Mock()
    import src.medhalib.Sensors.Image as Image

    img = Image.CameraModule("MAX", 0, "test.png")
    img.capture()
    img.capture("test.jpg")

  def test_CameraModule_capturefile(self):
    sys.modules['picamera'] = Mock()
    import src.medhalib.Sensors.Image as Image

    imgfile = os.path.join(os.getcwd(), "tests", "testimg.jpg")
    img = Image.CameraModule("MAX", 0, imgfile)
    img.get_base64_image()
    img.cleanup()

    

if __name__ == '__main__':
  unittest.main()