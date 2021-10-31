#! /usr/bin/env python3

import rospy

from std_msgs.msg import String, Int32
from robot_driver.motor_driver import MotorDriver

class MotorDriverROSWrapper:
	
	def __init__(self):
		rospy.Subscriber("movement", String, self.callback_movement)
		publish_current_speed_frequency = rospy.get_param("~publish_current_speed_frequency", 5.0)
		self.motor = MotorDriver(max_speed = 8)
		self.current_speed = rospy.Publisher("current_speed", Int32, queue_size=10)
		
		rospy.Timer(rospy.Duration(1.0/publish_current_speed_frequency), self.publish_current_speed)
	
	def publish_current_speed(self, event = None):
		self.current_speed.publish(self.motor.get_speed())	
		
	def callback_movement(self,msg):
		a = list(msg.data)
		b = a[0]+a[1]
		self.motor.set_speed(5)
		print("Success move to %s" %b)
		
if __name__ == "__main__":
	rospy.init_node("motor_driver")
	
	motor_driver_wrapper = MotorDriverROSWrapper()
	rospy.loginfo("Motor driver is now started, ready to get commands")
	rospy.spin()
