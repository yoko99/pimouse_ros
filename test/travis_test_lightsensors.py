#!/usr/bin/env python
#encoding: utf8
import unittest, rostest
import rosnode, rospy
import time
from pimouse_ros.msg import LightSensorValues

class LightsensorTest(unittest.TestCase):
    def setUp(self):
        self.count = 0
        rospy.Subscriber('/lightsensors', LightSensorValues, self.callback)
        self.values = LightSensorValues()

    def callback(self,data):
        self.count +=1
        self.values = data

    def check_values(self,lf,ls,rs,rf):
        vs = self.values
        # print vs.right_forward
        self.assertEqual(vs.left_forward, lf, "different value: left_forward")
        self.assertEqual(vs.left_side, ls, "different value: left_side")
        self.assertEqual(vs.right_side, rs, "different value: right_side")
        self.assertEqual(vs.right_forward,lf,"different value: right_forward")
        self.assertEqual(vs.sum_all, lf+ls+rs+rf, "different value: sum_all")
        self.assertEqual(vs.sum_forward, lf+rf, "different value: sum_forward")

    def test_node_exist(self):
        nodes = rosnode.get_node_names()
        self.assertIn('/lightsensors', nodes, "node dose not exist")

    def test_get_value(self):
        rospy.set_param('/lightsensors_freq', 10)
        time.sleep(2)
        with open("/dev/rtlightsensor0", "w") as f:
            f.write("1 10 1 1\n")

        time.sleep(3)
        self.assertFalse(self.count == 0, "cannnot subscribe the topic")
        self.check_values(1,1,10,1)

    def test_change_parameter(self):
        rospy.set_param('lightsensors_freq', 1)
        time.sleep(2)
        c_prev = self.count
        time.sleep(3)
        self.assertTrue(self.count < c_prev + 4, "freq dose not change")
        self.assertFalse(self.count == c_prev, "cubscriber is stopped")

if __name__ == '__main__':
    time.sleep(3)
    rospy.init_node('travis_test_lightsensors')
    rostest.rosrun('pomouse_ros','travis_test_lightsensors', LightsensorTest)
