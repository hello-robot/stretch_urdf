#!/bin/bash

echo "Prior to running this script make sure you rpl, which can be installed with sudo apt install rpl."
echo ""

OLD_NAME="package://stretch_description/"
NEW_NAME="./"

ros2 run xacro xacro ./urdf/stretch_description_RE2V0_tool_none.xacro >> ./urdf/stretch_description_RE2V0_tool_none.urdf
rpl -q --encoding UTF-8 $OLD_NAME $NEW_NAME ./urdf/stretch_description_RE2V0_tool_none.urdf



## Copy D435i mesh from the realsense2_description ROS package to the exported URDF.
#echo "Copy D435i mesh from the realsense2_description ROS package to the exported URDF."
#echo "cp `rospack find realsense2_description`/meshes/d435.dae ./exported_urdf/meshes/"
#cp `rospack find realsense2_description`/meshes/d435.dae ./exported_urdf/meshes/
#echo "rpl "package://realsense2_description/" "./" ./exported_urdf/stretch.urdf"
#rpl -q --encoding UTF-8 "package://realsense2_description/" "./" ./exported_urdf/stretch.urdf
#echo ""


