#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def call():
    call_pub = rospy.Publisher('chatter', data_class=String, queue_size=10)
    rospy.init_node('call', anonymous=True)
    rate = rospy.Rate(1)
    count = 0
    while not rospy.is_shutdown():
        mess = "Hello bro %s" %count
        rospy.loginfo(mess)
        call_pub.publish(mess)
        rate.sleep()
        count += 1

if __name__ == "__main__":
    try:
        call()
    except rospy.ROSInterruptException:
        pass