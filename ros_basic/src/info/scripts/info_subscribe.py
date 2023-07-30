#!/usr/bin/env python

import rospy
from ros_basic.msg import Info

def subscribe(data : Info):
    rospy.loginfo(data)

if __name__ == "__main__":
    try:
        rospy.init_node('info_subscribe', anonymous=True)
        rospy.Subscriber('info_topic', Info, callback=subscribe)
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated!!")