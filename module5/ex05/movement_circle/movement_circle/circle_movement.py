import math

from geometry_msgs.msg import Twist, Pose

import rclpy
from rclpy.node import Node
from tf2_msgs.msg import TFMessage
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

from turtlesim.srv import Spawn

import time


# class FrameListener(Node):

#     def __init__(self):
#         super().__init__('robot_frame_listener')
#         self.publisher = self.create_publisher(Twist, '/robot/cmd_vel', 1)


#         self.timer = self.create_timer(0.1, self.on_timer)

#     def on_timer(self):

#         msg = Twist()
#         scale_forward_speed = 0.5
#         msg.linear.x = 0.5
        
#         msg.angular.z = 1.0
   
       
 

#         self.publisher.publish(msg)

class FrameListener(Node):
    
    def __init__(self):
        super().__init__('robot_frame_listener')
        self.publisher = self.create_publisher(Twist, '/robot/cmd_vel', 1)
        
        # Define the states for forward, u-turn, backward, and u-turn
        self.state = 'forward'
        self.start_time = self.get_clock().now().seconds_nanoseconds()[0]  # Record the start time
        self.duration = 2  # Duration for each movement state in seconds
        self.timer = self.create_timer(0.1, self.on_timer)

    def on_timer(self):
        msg = Twist()
        
        # Get the current time and calculate elapsed time in seconds
        current_time = self.get_clock().now().seconds_nanoseconds()[0]
        elapsed_time = current_time - self.start_time

        # Switch states based on elapsed time
        if self.state == 'forward':
            msg.linear.x = 0.5  # Move forward
            if elapsed_time > self.duration:
                self.state = 'u_turn'
                self.start_time = current_time

        elif self.state == 'u_turn':
            msg.angular.z = 0.1  # Rotate in place
            if elapsed_time > self.duration:
                self.state = 'backward'
                self.start_time = current_time

        elif self.state == 'backward':
            msg.linear.x = -0.5  # Move backward
            if elapsed_time > self.duration:
                self.state = 'u_turn_back'
                self.start_time = current_time

        elif self.state == 'u_turn_back':
            msg.angular.z = 0.1  # Rotate in place
            if elapsed_time > self.duration:
                self.state = 'forward'
                self.start_time = current_time  # Restart the cycle

        # Publish the message
        self.publisher.publish(msg)

def main():
    rclpy.init()
    node = FrameListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
