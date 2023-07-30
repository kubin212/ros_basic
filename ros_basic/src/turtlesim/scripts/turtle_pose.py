#!/usr/bin/env python

import rospy
from turtlesim.msg import Pose
from math import pi

def pose_callback(data : Pose):
    #data = Pose()
    rospy.loginfo("Position of robot x: %s, y: %s, theta: %s, vel :%s", str(data.x), str(data.y), str(data.theta*180/pi), str(data.linear_velocity))

def init():
    rospy.init_node('pose_sub', anonymous=True)
    rospy.Subscriber('/turtle1/pose', Pose, pose_callback)
    rospy.spin()

if __name__ ==  "__main__":
    try:
        init()
    except rospy.ROSInterruptException:
        rospy.loginfo("Terminated!!")