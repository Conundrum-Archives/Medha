import gc
import os
import time
import warnings
import medhaboard.Utils.LogModules as LogModule

# import mock while in development/debug mode
if ("DEBUGMODE" in os.environ):
  import Mock.GPIO as GPIO
else:
  import RPi.GPIO as GPIO

# initialize logger
log = LogModule.init_logger()


class Servo180:

  """
  Servo180 class contains functionality to set 180 degree servo to an angle.
  """

  def __init__(self, servo_pin):
    # pin values in GPIO.BCM numbers
    GPIO.setmode(GPIO.BCM)

    self.SERVO_PIN = servo_pin

    GPIO.setup(self.SERVO_PIN, GPIO.OUT)

    self.SERVO_PWM = GPIO.PWM(self.SERVO_PIN, 50)         # GPIO servo_pin for PWM with 50Hz
    self.SERVO_PWM.start(0)                               # Initialization


  # methog to convert angle to cycles
  def get_cycle_from_angle(self, angle):
    duty = angle / 18 + 2
    log.debug("Ange: {angle} -> Duty: {duty}".format(angle=angle, duty=duty))
    return duty


  def set_servo_angle(self, angle):
    # check that angle must be within 0-180
    if (angle < 0 or angle > 180):
      errmsg = "angle value must be between 0 to 180. supplied: {angle}".format(angle=angle)
      log.warning(errmsg)
      warnings.warn(errmsg)
    else:
      log.debug(LogModule.METHOD_ENTRY)

      # set SERVO_PIN to output mode
      GPIO.output(self.SERVO_PIN, True)

      self.SERVO_PWM.ChangeDutyCycle(self.get_cycle_from_angle(angle))
      time.sleep(1)

      # turn off SERVO_PIN output mpde
      GPIO.output(self.SERVO_PIN, False)
      self.SERVO_PWM.ChangeDutyCycle(0)

      log.debug(LogModule.METHOD_EXIT)
