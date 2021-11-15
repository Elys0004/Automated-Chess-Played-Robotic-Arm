#! /usr/bin/env/ python

import sys
import rospy
import moveit_commander
import geometry_msgs.msg

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

robot = moveit_commander.RobotCommander()

arm_group = moveit_commander.MoveGroupCommander("arm")
arm_group.set_named_target("straight")
plan1 = arm_group.go()

rospy.sleep(5)
moveit_commander.roscpp_shutdown()

