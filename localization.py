import sys

from utilities import Logger

from rclpy.time import Time

from utilities import euler_from_quaternion, calculate_angular_error, calculate_linear_error
from rclpy.node import Node
from geometry_msgs.msg import Twist

from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from nav_msgs.msg import Odometry as odom

from sensor_msgs.msg import Imu
from kalman_filter import kalman_filter

from rclpy import init, spin, spin_once

import numpy as np
import message_filters

rawSensors=0
kalmanFilter=1
odom_qos=QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT, durability=DurabilityPolicy.VOLATILE, history=HistoryPolicy.KEEP_LAST, depth=10)

class localization(Node):
    
    def __init__(self, type, dt, loggerName="robotPose.csv", loggerHeaders=["imu_ax", "imu_ay", "kf_ax", "kf_ay","odom_v", "odom_w", "kf_vx","kf_w", "odom_x", "odom_y", "kf_x", "kf_y","odom_th", "kf_th","stamp"]):

        super().__init__("localizer")

        self.loc_logger=Logger( loggerName , loggerHeaders)
        self.pose=None
        
        if type==rawSensors:
            self.initRawSensors()
        elif type==kalmanFilter:
            self.initKalmanfilter(dt)
        else:
            print("We don't have this type for localization", sys.stderr)
            return  

    def initRawSensors(self):
        self.create_subscription(odom, "/odom", self.odom_callback, qos_profile=odom_qos)
        
    def initKalmanfilter(self, dt):
        
        # TODO Part 3: Set up the quantities for the EKF (hint: you will need the functions for the states and measurements)
        
        x= [0,0,0,0,0,0]
        
        Q= 0.2*np.identity(6)
   
        R= np.matrix([[0.5, 0.0, 0.0, 0.0],
                     [0.0, 0.5, 0.0, 0.0],
                     [0.0, 0.0, 20.0, 0.0],
                     [0.0, 0.0, 0.0, 20.0]]).A


        P= np.identity(6) # initial covariance
        
        self.kf=kalman_filter(P,Q,R, x, dt)

        # TODO Part 3: Use the odometry and IMU data for the EKF
        self.odom_sub=message_filters.Subscriber(self, odom, '/odom', qos_profile=odom_qos)
        self.imu_sub=message_filters.Subscriber(self, Imu, '/imu', qos_profile=odom_qos)
        
        time_syncher=message_filters.ApproximateTimeSynchronizer([self.odom_sub, self.imu_sub], queue_size=10, slop=0.1)
        time_syncher.registerCallback(self.fusion_callback)
    
    def fusion_callback(self, odom_msg: odom, imu_msg: Imu):
        
        # TODO Part 3: Use the EKF to perform state estimation
        # Take the measurements
        # your measurements are the linear velocity and angular velocity from odom msg
        # and linear acceleration in x and y from the imu msg
        # the kalman filter should do a proper integration to provide x,y and filter ax,ay
        z=[ odom_msg.twist.twist.linear.x,
            odom_msg.twist.twist.angular.z,
            imu_msg.linear_acceleration.x,
            imu_msg.linear_acceleration.y]
        
        # Implement the two steps for estimation
        self.kf.predict()
        self.kf.update(z)
        
        # Get the estimate
        xhat=self.kf.get_states()

        # Update the pose estimate to be returned by getPose
        self.pose=[xhat[0], xhat[1], xhat[2], odom_msg.header.stamp]

        measurementModel = self.kf.measurement_model()
        # TODO Part 4: log your data
        self.loc_logger.log_values([z[2], z[3], measurementModel[2], measurementModel[3], z[0], z[1], xhat[4], xhat[3], odom_msg.pose.pose.position.x, 
                                    odom_msg.pose.pose.position.y, xhat[0], xhat[1], euler_from_quaternion(odom_msg.pose.pose.orientation), xhat[2], Time.from_msg(odom_msg.header.stamp).nanoseconds])
      
    def odom_callback(self, pose_msg):
        
        self.pose=[ pose_msg.pose.pose.position.x,
                    pose_msg.pose.pose.position.y,
                    euler_from_quaternion(pose_msg.pose.pose.orientation),
                    pose_msg.header.stamp]

    # Return the estimated pose
    def getPose(self):
        return self.pose


if __name__=="__main__":
    
    init()
    
    LOCALIZER=localization(type=kalmanFilter, dt=0.1)
    
    spin(LOCALIZER)
