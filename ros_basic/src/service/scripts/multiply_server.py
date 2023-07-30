#!/usr/bin/env python

from ros_basic.srv import Multiply2Ints
#from ros_basic.srv import Multiply2IntsRequest
from ros_basic.srv import Multiply2IntsResponse
import rospy

def handle_multiply_2_ints(request):
    rospy.loginfo("Result: %s", str(request.a * request.b))
    return Multiply2IntsResponse(request.a * request.b)


def multiply():
    rospy.init_node('multiply_2_ints_server', anonymous=True)
    serve = rospy.Service('multiply_2_ints', Multiply2Ints, handler=handle_multiply_2_ints)
    print("Ready to reply")
    rospy.spin()


if __name__ == "__main__":
    multiply()