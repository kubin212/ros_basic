#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt

class turtleBot:
    def __init__(self):
        rospy.init_node("turtle_control", anonymous=True)
        self.vel_pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
        self.pose_sub = rospy.Subscriber("/turtle1/pose", Pose, callback=self.update_pose)
        self.pose = Pose()
        self.rate = rospy.Rate(10)

    def update_pose(self, data:Pose):
        self.pose = data
        self.pose.x = round(self.pose.x, 2)
        self.pose.y = round(self.pose.y, 2)

    def dist(self, goal_pose:Pose):
        dist_x = goal_pose.x - self.pose.x
        dist_y = goal_pose.y - self.pose.y
        dist = sqrt(pow(dist_x, 2) + pow(dist_y, 2))
        return dist
    
    def linear_vel(self, goal_pose:Pose, Kv=1.5):
        vel = Kv*self.dist(goal_pose)
        return vel
    
    def steering_angle(self, goal_pose:Pose):
        angle = atan2(goal_pose.y-self.pose.y, goal_pose.x-self.pose.x)
        return angle

    def angular_vel(self, goal_pose:Pose, Ko=6):
        vel = Ko*(self.steering_angle(goal_pose) - self.pose.theta)
        return vel
    
    def move_to_goal(self):
        goal_pose = Pose()
        goal_pose.x = float(input("Set x: "))
        goal_pose.y = float(input("Set y: "))
        dist_tolerance = float(input("Set tolerance: "))
        vel_msg = Twist()

        while self.dist(goal_pose) >= dist_tolerance:
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.angular.z = self.angular_vel(goal_pose)

            self.vel_pub.publish(vel_msg)
            self.rate.sleep()

        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.vel_pub.publish(vel_msg)
        rospy.loginfo("x: %s, y: %s", str(self.pose.x), str(self.pose.y))
        ask = str(input("Continue? "))
        if ask == "y":
            self.move_to_goal()
        else:
            rospy.ROSInterruptException
            rospy.loginfo("Node terminated!!")
        # rospy.spin()

if __name__ == "__main__":
    try:
        x = turtleBot()
        x.move_to_goal()
    except rospy.ROSInterruptException:
        pass                 