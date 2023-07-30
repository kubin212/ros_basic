#!/usr/bin/env python

from ros_basic.srv import Multiply2Ints
from ros_basic.srv import Multiply2IntsRequest
from ros_basic.srv import Multiply2IntsResponse
import rospy
import sys

def multiply_2_ints_client(x, y):
    rospy.wait_for_service('multiply_2_ints')
    try:
        multiply_2_ints = rospy.ServiceProxy('multiply_2_ints', Multiply2Ints)
        result = multiply_2_ints(x, y)
        return result.product
    except rospy.ServiceException as e:
        rospy.loginfo("Service call failed %s"%(e))

def usage():
    mess = "%s"%sys.argv[0]
    return mess

if __name__ == "__main__":
    if len(sys.argv) == 3:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    else:
        print(usage())
        sys.exit(1)
    print("Requesting %s+%s"%(x, y))
    print("Received: %s"%(multiply_2_ints_client(x, y)))