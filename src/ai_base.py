#! /usr/bin/env python

import roslib; roslib.load_manifest('capra_ai')
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
from capra_msgs.msg import AiStatus, EStopStatus

class AIBase(object):
    running = True
    
    def __init__(self, node_name):
        rospy.init_node(node_name)
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        
    def run(self):
        #self.client.wait_for_server()
        self._create_status_broadcaster()
        rospy.Subscriber("/capra_smartmotor/estop", EStopStatus, self._estop_subscriber)

    def _create_status_broadcaster(self):
        self.status_publisher = rospy.Publisher('~status', AiStatus)
        rospy.Timer(rospy.Duration(0.2), self._status_broadcaster)

    def _status_broadcaster(self, event):
        status = AiStatus()
        status.isRunning = self.running
        self.status_publisher.publish(status)

    def _estop_subscriber(self, data):
        self.estop_listener(data.stopped)

    def send_goal(self, goal, wait=False):
        self.client.send_goal(goal)
        
        if wait:
            self.client.wait_for_result()

    def get_state(self):
        return self.client.get_state()

    def estop_listener(self, status):
        self.running = status
                