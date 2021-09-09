#!/usr/bin/env python

import rospy
import random
from rt1_ass1.srv import Destination , DestinationResponse

#to generate the new destination point for the robot this robot plays the role... 

def random_targ(req):                        
    
    rospy.loginfo('Tbctl_goal call')    
    x_destination = random.uniform(-6.0, 6.0)
    y_destination = random.uniform(-6.0, 6.0)
    print("$$$$$feedback of the server$$$$$")
    print(x_destination, y_destination)
    return DestinationResponse(x_destination,y_destination)


rospy.init_node('tbctl_goal')
#Service of this node 
rospy.Service('tbctl_goal', Destination, random_targ)
rospy.spin()

