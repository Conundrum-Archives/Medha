import gc
import os
import time
import medhaboard.Utils.LogModules as LogModule

# import mock while in development/debug mode
if ("DEBUGMODE" in os.environ):
  import Mock.GPIO as GPIO
else:
  import RPi.GPIO as GPIO

# initialize logger
log = LogModule.init_logger()

class UltraSonicSensor:

  """
  UltraSonicSensor class implements interface for ultrasonic sensor module.
  """

  def __init__(self, trig_pin, echo_pin):
    # pin values in GPIO.BCM numbers
    GPIO.setmode(GPIO.BCM)

    self.TRIGGER_PIN = trig_pin
    self.ECHO_PIN = echo_pin

    GPIO.setup(self.TRIGGER_PIN, GPIO.OUT)
    GPIO.setup(self.ECHO_PIN, GPIO.IN)

  # method that gets distance value from sensor
  def get_distance(self):
    log.debug(LogModule.METHOD_ENTRY)

    GPIO.output(self.TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(self.TRIGGER_PIN, False)
    start_time = 0
    stop_time = 0
    timeout = 20
    timeoutstart = time.time()

    while GPIO.input(self.ECHO_PIN) == 0 and (time.time() - timeoutstart) <= timeout:
      start_time = time.time()

    while GPIO.input(self.ECHO_PIN) == 1 and (time.time() - timeoutstart) <= timeout:
      stop_time = time.time()

    distance = ((stop_time - start_time) * 34300) / 2

    del start_time
    del stop_time
    log.debug(LogModule.METHOD_EXIT)

    return distance

  # method to cleanup sensor resources
  def cleanup(self):
    log.debug("cleaning GPIO pins from Ultrasonic sensor module")
    GPIO.cleanup()
