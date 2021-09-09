#!/usr/bin/env python

import rospy
import math
import random
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from rt1_ass1.srv import Destination




#Initialize state of the robot in the 2d simulator
x_pose = 0.0
y_pose = 0.0

#This value is for thresold on the robots end point for the goal
speed_th = 0.1
speed_gain = 0.5

#reads the position of the robot from the odometery topic
def my_odom(msg):

   
    #Define global varaibles
    global x_pose
    global y_pose
    #Read the values
    x_pose = msg.pose.pose.position.x
    y_pose = msg.pose.pose.position.y


def main():

    
    
    #To Create a subscriber to the odometry function
    odo_sub = rospy.Subscriber("odom", Odometry,my_odom)
    #To Create a publisher and its role is to update the speed of the robot
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    rate = rospy.Rate(10) # 10hz

    #Create the service client  
    restart = rospy.ServiceProxy('tbctl_goal', Destination)

    while not rospy.is_shutdown():	
        
     	# Create an distance request of the client
    	print("/////destination requested/////.")
    
    	rospy.wait_for_service('tbctl_goal')
    	try: 
    	    rst = restart()
	    print("/////destination reached/////:")
    	    x_destination = rst.x_destination
    	    y_destination = rst.y_destination
    	    print(x_destination, y_destination)
    	except rospy.ServiceException as e:
	    print("/////Service call failed/////: %s" %e)   
	
    	# distance in between the robot and the destination is requested	
    	distance_x = (x_destination-x_pose)
    	distance_y = (y_destination-y_pose)    
    	distance = math.sqrt(distance_x**2 + distance_y**2)
    
     
    	# while the distance is below the threshold
    	# evaluate the distance in between the target and the robot and update the speed
    	while distance > speed_th:

            # The speed of the robot is evaluated
            speed_x = speed_gain * distance_x
            speed_y = speed_gain * distance_y

      	    #And the speed is published
	    twist = Twist()
	    twist.linear.x = speed_x
	    twist.linear.y = speed_y        

	    pub.publish(twist)

            #this is to update the robot position
    	    distance_x = (x_destination-x_pose)
    	    distance_y = (y_destination-y_pose)    
    	    distance = math.sqrt(distance_x**2 + distance_y**2)

        #once the robot reached the target
    	print('/////Desination reached by the turtle bot///// :)')
    
        
if __name__ == '__main__':

    try:
	#initialize the node
	# anonymous is True to ahve more than a listener
    	rospy.init_node("turtlebot_controller", anonymous="True",disable_signals=True)
     	main()	
	rate.sleep()
    except KeyboardInterrupt:
	print("Out")
