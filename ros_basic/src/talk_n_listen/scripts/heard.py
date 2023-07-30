#!/usr/bin/env python

import rospy
from std_msgs.msg import String

#count = 0

def heard(mess):
    # global count
    # count += 1
    rospy.loginfo("Hear: %s", mess.data)

def init():
    rospy.Subscriber(name='chatter', data_class=String, callback=heard)
    rospy.init_node('heard', anonymous=True)
    rospy.spin()


if __name__ == "__main__":
    try:
        init()
    except rospy.ROSInterruptException:
        pass