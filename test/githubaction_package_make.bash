#!/bin/bash -xve

#sync and make
rsync -av ./ ~/work/catkin_ws/src/pimouse_ros/
cd ~/work/catkin_ws
catkin_make
