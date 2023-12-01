#! /usr/bin/env python

import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Header
from sensor_msgs.msg import JointState
from intera_core_msgs.srv import SolvePositionFK, SolvePositionFKRequest

# defining desired positions
aboveAR = np.array([1.22222, 0.87835, -1.48364, 1.73790, 2.36236, -0.01118, 3.34471])
aboveGrid = np.array([-0.03083, -0.59538, 0.04406, 1.55704, -0.07918, -1.023679, 3.30380])
aboveHand = np.array([0.52847, -0.28549, -0.17221, 1.23390, 0.47744, -0.97401, 3.17143])

def fk_service_client():
    service_name = "ExternalTools/right/PositionKinematicsNode/FKService"
    fk_service_proxy = rospy.ServiceProxy(service_name, SolvePositionFK)
    fk_request = SolvePositionFKRequest()
    joints = JointState()
    # YOUR CODE HERE
    joints.name = ['right_j0', 'right_j1', 'right_j2', 'right_j3','right_j4', 'right_j5', 'right_j6']
    #joint_input = [float(i) for i in input("Enter 7 joint angles with a space in between each entry: ").split(" ")]
    joints.position = aboveAR
    # Add desired pose for forward kinematics
    fk_request.configuration.append(joints)
    # Request forward kinematics from base to "right_hand" link
    fk_request.tip_names.append('right_hand')

    try:
        rospy.wait_for_service(service_name, 5.0)
        response = fk_service_proxy(fk_request)
    except (rospy.ServiceException, rospy.ROSException) as e:
        rospy.logerr("Service call failed: %s" % (e,))
        return 

    # Check if result valid
    if (response.isValid[0]):
        rospy.loginfo("SUCCESS - Valid Cartesian Solution Found")
        rospy.loginfo("\nFK Cartesian Solution:\n")
        rospy.loginfo("------------------")
        rospy.loginfo("Response Message:\n%s", response)
    else:
        rospy.logerr("INVALID JOINTS - No Cartesian Solution Found.")
        return 

    return True


def main():
    rospy.init_node("fk_service_client")

    fk_service_client()

if __name__ == '__main__':
    main()