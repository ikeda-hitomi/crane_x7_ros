#!/usr/bin/env python
# coding: utf-8
#シミュレータ用(つかむときのグリッパーの角度：23.5度)
#実機用(objectがやわらかいから10度)

import rospy
import time
import actionlib
from control_msgs.msg import (
    FollowJointTrajectoryAction,
    FollowJointTrajectoryGoal
)
from control_msgs.msg import (      
    GripperCommandAction,
    GripperCommandGoal
 )
from trajectory_msgs.msg import JointTrajectoryPoint
import math
import sys
import numpy as np

class ArmJointTrajectoryExample(object):
    def __init__(self):
        self._client = actionlib.SimpleActionClient(
            "/crane_x7/arm_controller/follow_joint_trajectory", FollowJointTrajectoryAction)
        rospy.sleep(0.1)
        if not self._client.wait_for_server(rospy.Duration(secs=5)):
            rospy.logerr("Action Server Not Found")
            rospy.signal_shutdown("Action Server Not Found")
            sys.exit(1)

        self.gripper_client = actionlib.SimpleActionClient("/crane_x7/gripper_controller/gripper_cmd",GripperCommandAction)
        self.gripper_goal = GripperCommandGoal()
        # Wait 5 Seconds for the gripper action server to start or exit
        self.gripper_client.wait_for_server(rospy.Duration(5.0))
        if not self.gripper_client.wait_for_server(rospy.Duration(5.0)):
            rospy.logerr("Exiting - Gripper Action Server Not Found.")
            rospy.signal_shutdown("Action Server not found.")
            sys.exit(1)
    
    def go(self, mode):
        #どっち投げかを表示 
        if mode > 0.5:
            pitching_mode = "left"
        else:
            pitching_mode = "right"
        print "pitching_mode:"+pitching_mode

        #つかむ準備 手先座標( 0.2, 0 0.2)
        point = JointTrajectoryPoint()
        goal = FollowJointTrajectoryGoal()
     
        goal.trajectory.joint_names = ["crane_x7_shoulder_fixed_part_pan_joint", "crane_x7_shoulder_revolute_part_tilt_joint",
                                       "crane_x7_upper_arm_revolute_part_twist_joint", "crane_x7_upper_arm_revolute_part_rotate_joint",
                                       "crane_x7_lower_arm_fixed_part_joint", "crane_x7_lower_arm_revolute_part_joint",
                                       "crane_x7_wrist_joint",]
      
        joint_values = [0.21304366673905673, 0.02974849165462512, -0.20838138537767303, -2.197273761794529, -0.00897299687593378, -0.9915954713398651, -1.5583097453428332]
       
        position = math.radians(45.0)
        effort  = 1.0
        self.gripper_goal.command.position = position
        self.gripper_goal.command.max_effort = effort
                
        for i, p in enumerate(joint_values):
            point.positions.append(p)
        
        point.time_from_start = rospy.Duration(secs=2.0)
        goal.trajectory.points.append(point)
        self._client.send_goal(goal)

        self.gripper_client.send_goal(self.gripper_goal,feedback_cb=self.feedback)
        self._client.wait_for_result(timeout=rospy.Duration(100.0))
        
        #つかむとき 手先座標( 0.2, 0, 0.1) 
        point = JointTrajectoryPoint()
        goal = FollowJointTrajectoryGoal()

        goal.trajectory.joint_names = ["crane_x7_shoulder_fixed_part_pan_joint", "crane_x7_shoulder_revolute_part_tilt_joint",
                                       "crane_x7_upper_arm_revolute_part_twist_joint", "crane_x7_upper_arm_revolute_part_rotate_joint",
                                       "crane_x7_lower_arm_fixed_part_joint", "crane_x7_lower_arm_revolute_part_joint",
                                       "crane_x7_wrist_joint",]
         
        joint_values = [0.1721327091256155, -0.3630645331662308, -0.1862058852524493, -2.3243098124547927, 0.130925888195077, -0.48587059161714485, -1.6908899687220424]
       
        position = math.radians(23.5) #つかむときのgripperの角度(実機:10.0, シミュレータ:23.5)
        effort  = 1.0
        self.gripper_goal.command.position = position
        self.gripper_goal.command.max_effort = effort
                
        for i, p in enumerate(joint_values):
            point.positions.append(p)
        
        point.time_from_start = rospy.Duration(secs=2.0)
        goal.trajectory.points.append(point)
        self._client.send_goal(goal)
        
        rospy.sleep(2.5)
        
        self.gripper_client.send_goal(self.gripper_goal,feedback_cb=self.feedback)
        self._client.wait_for_result(timeout=rospy.Duration(100.0))
        rospy.sleep(1.0)

        #投げる準備 
        point = JointTrajectoryPoint()
        goal = FollowJointTrajectoryGoal()

        goal.trajectory.joint_names = ["crane_x7_shoulder_fixed_part_pan_joint", "crane_x7_shoulder_revolute_part_tilt_joint",
                                       "crane_x7_upper_arm_revolute_part_twist_joint", "crane_x7_upper_arm_revolute_part_rotate_joint",
                                       "crane_x7_lower_arm_fixed_part_joint", "crane_x7_lower_arm_revolute_part_joint",
                                       "crane_x7_wrist_joint",]
        
        joint_values = [ 0.99, 1.42, 0.44, -1.25, -1.44, 0.67, 0.00]
        
        if mode == 1:
            for i in range(4):
                joint_values[i*2] = joint_values[i*2] * (-1)
                
        for i, p in enumerate(joint_values):
            point.positions.append(p)
        
        point.time_from_start = rospy.Duration(secs=2.0)
        goal.trajectory.points.append(point)
        self._client.send_goal(goal)
        self._client.wait_for_result(timeout=rospy.Duration(100.0))

        #中間点 
        point = JointTrajectoryPoint()
        goal = FollowJointTrajectoryGoal()

        goal.trajectory.joint_names = ["crane_x7_shoulder_fixed_part_pan_joint", "crane_x7_shoulder_revolute_part_tilt_joint",
                                       "crane_x7_upper_arm_revolute_part_twist_joint", "crane_x7_upper_arm_revolute_part_rotate_joint",
                                       "crane_x7_lower_arm_fixed_part_joint", "crane_x7_lower_arm_revolute_part_joint",
                                       "crane_x7_wrist_joint",]
        
        joint_values = [ 2.15, 1.22, 0.08, -1.45, -1.95, 0.24, 0.00]

        if mode == 1:
            for i in range(4):
                joint_values[i*2] = joint_values[i*2] * (-1)

        for i, p in enumerate(joint_values):
            point.positions.append(p)
        
        point.time_from_start = rospy.Duration(secs=0.6)
        goal.trajectory.points.append(point)
        self._client.send_goal(goal)
        self._client.wait_for_result(timeout=rospy.Duration(100.0))
       
        #なげるとき
        point = JointTrajectoryPoint()
        goal = FollowJointTrajectoryGoal()

        goal.trajectory.joint_names = ["crane_x7_shoulder_fixed_part_pan_joint", "crane_x7_shoulder_revolute_part_tilt_joint",
                                       "crane_x7_upper_arm_revolute_part_twist_joint", "crane_x7_upper_arm_revolute_part_rotate_joint",
                                       "crane_x7_lower_arm_fixed_part_joint", "crane_x7_lower_arm_revolute_part_joint",
                                       "crane_x7_wrist_joint",]
        
        joint_values = [ 2.59, 1.14, -1.57, -0.88, -1.15, -0.32, -0.08]
       
        if mode == 1:
            for i in range(4):
                joint_values[i*2] = joint_values[i*2] * (-1)
        
        position = math.radians(50.0)
        effort  = 1.0
        self.gripper_goal.command.position = position
        self.gripper_goal.command.max_effort = effort
                
        for i, p in enumerate(joint_values):
            point.positions.append(p)
        
        point.time_from_start = rospy.Duration(secs=0.2)
        goal.trajectory.points.append(point)
        self._client.send_goal(goal)
        
        rospy.sleep(0.05)#何秒後にグリッパーを開くか
        
        self.gripper_client.send_goal(self.gripper_goal,feedback_cb=self.feedback)
        self._client.wait_for_result(timeout=rospy.Duration(100.0))
        
    def feedback(self,msg):
        print("feedback callback")

if __name__ == "__main__":
    rospy.init_node("arm_joint_trajectory_example")
    arm_joint_trajectory_example = ArmJointTrajectoryExample()
    
    while 1 :
        mode = input("右投げの場合 0, 左投げの場合 1を入力\n pitching_mode: ")
        if mode == 0 or mode == 1 :
            break
        else :
            print("Error\n")
    
    arm_joint_trajectory_example.go(mode)
