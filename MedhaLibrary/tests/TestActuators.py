import unittest
import src.medhalib.Actuators.Servo as Servo


class TestServo(unittest.TestCase):

  """TEST Servo class and methods"""

  @classmethod
  def setUpClass(self):
    self.servo = Servo.Servo180(10)

  def test_Servo180_get_cycle_from_angle(self):
    self.assertEqual(self.servo.get_cycle_from_angle(18), 3.0)
    self.assertEqual(self.servo.get_cycle_from_angle(36), 4.0)

  def test_Servo180_set_servo_angle(self):
    self.assertWarns(UserWarning, self.servo.set_servo_angle, 181)
    self.assertWarns(UserWarning, self.servo.set_servo_angle, 500)
    self.assertWarns(UserWarning, self.servo.set_servo_angle, -1)
    self.assertWarns(UserWarning, self.servo.set_servo_angle, -500)
    self.assertEqual(self.servo.set_servo_angle(0), None)

if __name__ == '__main__':
  unittest.main()