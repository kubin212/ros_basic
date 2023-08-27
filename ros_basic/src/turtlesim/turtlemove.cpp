#include "ros/ros.h"
#include "std_msgs/String.h"
#include "turtlesim/Pose.h"
#include "geometry_msgs/Twist.h"
#include "math.h"
#include <sstream>

using namespace std;
using namespace ros;
using namespace std_msgs;
using namespace geometry_msgs;
using namespace turtlesim;

class Turtle
{   
private:
    Publisher vel_pub;
    Subscriber pose_sub;
    Pose pose;
    double x,y,tolerance;
    String msg;

public:
    Turtle()
    {
        NodeHandle n;
        this->vel_pub = n.advertise<Twist>("/turtle1/cmd_vel", 10);
        this->pose_sub = n.subscribe("turtle1/pose", 10, &Turtle::update_pose, this);
    }

    void update_pose(const Pose::ConstPtr &msg)
    {
        this->pose.x = round(msg->x*100.0)/100.0;
        this->pose.y = round(msg->y*100.0)/100.0;
        this->pose.theta = round(msg->theta*100.0)/100.0;
    }

    double dist(const Pose &goal_pose)
    {
        double delta_x, delta_y, distance;
        delta_x = goal_pose.x - this->pose.x;
        delta_y = goal_pose.y - this->pose.y;
        distance = sqrt(delta_x*delta_x + delta_y*delta_y);
        return distance;
    }

    double linear_vel(const Pose &goal_pose, const double Kp)
    {
        double vel;
        vel = Kp*(this->dist(goal_pose));
        return vel;
    }

    double steering_angle(const Pose &goal_pose)
    {
        double delta_x, delta_y, angle;
        delta_x = goal_pose.x - this->pose.x;
        delta_y = goal_pose.y - this->pose.y;
        angle = atan2(delta_y, delta_x);
        return angle;
    }

    double angular_vel(const Pose &goal_pose, const double Kp)
    {
        double vel;
        vel = Kp*(this->steering_angle(goal_pose) - this->pose.theta);
        return vel;
    }

    void move2goal()
    {
        Pose goal_pose;
        Twist vel_msg;
        Rate loop(10);
        cout << "Target x: "; cin >> x;
        cout << "Target y: "; cin >> y;
        goal_pose.x = x;
        goal_pose.y = y;
        cout << "Tolerance: "; cin >> tolerance;

        while (this->dist(goal_pose) >= tolerance)
        {
            vel_msg.linear.x = this->linear_vel(goal_pose, 0.5);
            vel_msg.angular.z = this->angular_vel(goal_pose, 4);

            this->vel_pub.publish(vel_msg);
            //ROS_INFO("%lf", vel_msg.angular.z);
            spinOnce();
            loop.sleep();
        }

        vel_msg.linear.x = 0.00;
        vel_msg.angular.z = 0.00;
        this->vel_pub.publish(vel_msg);
        stringstream ss;
        ss << this->pose.x << " " << this->pose.y;
        msg.data = ss.str();
        ROS_INFO("%s", msg.data.c_str());
    }

    void SpiralClean(double omega)
    {
        Twist vel_msg;
        double radius = 0.00;
        while(radius < 3.00)
        {
            radius += 1.00;
            vel_msg.linear.x = radius;
            vel_msg.angular.z = omega;
            this->vel_pub.publish(vel_msg);
            spinOnce();
            Rate loop(1);
            loop.sleep();
        }
        vel_msg.linear.x = 0.00;
        vel_msg.angular.z = 0.00;
        this->vel_pub.publish(vel_msg);
    }
};

int main(int argc, char **argv)
{
    init(argc, argv, "robot_cleaner");
    Turtle bot = Turtle();
    bot.move2goal();
    bot.SpiralClean(7);
    spin();
    return 0;
}