#!/usr/bin/env python

import rospy
from ros_basic.msg import Info
import random

tennis = {"Djokovic":35, "Nadal":37, "Federer":41, "Murray":35}
ranking = [1,2,3,4]

def publish():
    pub = rospy.Publisher('info_topic', Info, queue_size=10)
    rospy.init_node('info_pub', anonymous=True)
    rate = rospy.Rate(1)

    global tennis
    global ranking
    while not rospy.is_shutdown():
        info_msg = Info()
        info_msg.name = list(tennis)[random.randint(0, len(tennis)-1)]
        info_msg.rank = ranking[random.randint(0, len(ranking)-1)]
        info_msg.age = tennis.get(info_msg.name)
        info_msg.score = random.randint(1, 1000)
        rospy.loginfo(info_msg)
        pub.publish(info_msg)
        rate.sleep()



if __name__ == "__main__":
    try:
        publish()
    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated!!")
