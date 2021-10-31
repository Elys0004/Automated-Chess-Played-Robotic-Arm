#!/usr/bin/env python3

from __future__ import print_function

import rospy
import roslib
import cv2
import sys
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image as ImageMsg
from PIL import Image


class image_converter:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera1/image_raw",ImageMsg,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "rgb8")
    except CvBridgeError as e:
      print(e)
    print(cv_image)
    crop_image = cv_image[260:540,260:540]
    resize = cv2.resize(crop_image,(800,800))
    print(resize.shape)
    im = Image.fromarray(resize)
    im.save(r'/home/elysia/catkin_ws/src/robot_driver/scripts/chess.png')
      
if __name__ == '__main__':
  rospy.init_node('image_converter')
  image_converter()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
    
""" Dosent work, can ignore
def callback(self,data):
	global image
	image = data

def __init__(self):
	self.image_pub = rospy.Publisher('stream', Image, queue_size = 10)
	self.bridge = CvBridge()
	self.image_sub = rospy.Subscriber('/camera1/raw_image', Image, callback)
	
def node():
	global image
	pub = rospy.Publisher('stream', Image, queue_size = 10)
	rospy.init_node('Camera')
	rate = rospy.Rate(10)
	sub = rospy.Subscriber('/camera1/raw_image', Image, callback)
	while not rospy.is_shutdown():
		opencv = self.CvBridge.imgmsg_to_cv2(img_msg = image, desired_encoding='passthrough')
		pub.publish(opencv)

if __name__ == '__main__':
	try:
		node()
	except rospy.ROSInterruptException:
		pass
	
"""

    
