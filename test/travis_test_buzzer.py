#!/usr/bin/env python
#encoding: utf8
import rospy, unittest, rostest, actionlib
import rosnode
import time
from std_msgs.msg import UInt16
from pimouse_ros.msg import MusicAction, MusicResult, MusicFeedback, MusicGoal

class BuzzerTest(unittest.TestCase):
    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('/buzzer' ,nodes, "node dose not exist")

    def test_put_value(self):
        pub = rospy.Publisher('/buzzer', UInt16, queue_size=10)
        for i in range(10):
            pub.publish(1234)
            time.sleep(0.1)

        with open("/dev/rtbuzzer0","r") as f:
            data = f.readline()
            print(f.read())
            self.assertEqual(data,"1234\n","value dose not written to rtbuzzer0")

if __name__ == '__main__':
    time.sleep(3)
    rospy.init_node('travis_test_buzzer')
    rostest.rosrun('pimouse_ros', 'travis_test_buzzer' ,BuzzerTest)
