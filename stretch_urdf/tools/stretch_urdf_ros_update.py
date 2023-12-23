#!/usr/bin/env python3

import os
import sys
from stretch_body.robot_params import RobotParams
import re
import stretch_body.hello_utils as hu
import shutil

root_dir = None
tool_name = RobotParams().get_params()[1]['robot']['tool']
model_name = RobotParams().get_params()[1]['robot']['model_name']

def get_ros_version():
    global root_dir
    if 'ROS_DISTRO' in os.environ.keys():
        if os.environ['ROS_DISTRO'] == 'noetic':
            # works on ubuntu 20.04
            import importlib_resources
            root_dir = str(importlib_resources.files("stretch_body"))
            print(f"Found ROS_DISTRO = noetic")
            return 1
        if os.environ['ROS_DISTRO'] == 'humble':
            # works on ubunut 22.04
            import importlib.resources as importlib_resources
            root_dir = importlib_resources.files("stretch_urdf")
            print(f"Found ROS_DISTRO = humble")
            return 2

hu.print_stretch_re_use()

ros_version = get_ros_version()
if ros_version is None:
    print("Unable to find a valid ROS Installation")
    sys.exit()

def make_uncalibrated_urdf(root_dir,filename):
    print("\nCopying URDF and Meshes to Stretch Description ROS package....")
    if root_dir:
        urdf_file = f"{root_dir}/{model_name}/{filename}"
        if os.path.isfile(urdf_file):
            with open(urdf_file, 'r') as file:
                lines = file.readlines()
        else:
            print(f"ERROR : Unable to find file = {urdf_file}")
            return
        
        updated_urdf_lines = []

        # Remove Link Ground
        found_link_ground = False
        for l in lines:
            if not found_link_ground and '<link name="link_ground">' in l:
                found_link_ground = True

            if not found_link_ground:
                updated_urdf_lines.append(l)

            if found_link_ground and '</joint>' in l:
                found_link_ground = False
        
        # Changes meshes path to address stretch_description package2 and remove collision STL references
        mesh_path_replaced_urdf_lines = []
        for line in updated_urdf_lines:
            if '<robot name="stretch">' in line:
                mesh_path_replaced_urdf_lines.append(re.sub('<robot name="stretch">', '<robot name="stretch_description">', line))
            
            if './meshes' in line:
                l = re.sub('./meshes', 'package://stretch_description/meshes', line)
                if '_collision.STL' in l:
                    l = re.sub('_collision.STL', '.STL', l)
                mesh_path_replaced_urdf_lines.append(l)
            else:
                mesh_path_replaced_urdf_lines.append(line)

        if ros_version==2:
            ros_repo_path = '/home/hello-robot/ament_ws/src/stretch_ros2'
        else:
            ros_repo_path = f'/home/hello-robot/catkin_ws/src/stretch_ros'
        
        ros_uncalibrated_urdf_path = f'{ros_repo_path}/stretch_description/urdf/stretch_uncalibrated.urdf'

        print(f"Writing URDF to path: {ros_uncalibrated_urdf_path}")
        with open(ros_uncalibrated_urdf_path, 'w') as file:
            for line in mesh_path_replaced_urdf_lines:
                file.write(line)
        print(f"Successfully copied Uncalibrated URDF to {ros_uncalibrated_urdf_path}")

        # Copy mesh files
        src_meshes_dir = f"{root_dir}/{model_name}/meshes"
        dst_meshes_dir = f"{ros_repo_path}/stretch_description/meshes"
        for f in os.listdir(src_meshes_dir):
            # ignore collision meshes
            if 'collision' not in f:
                shutil.copy(f"{src_meshes_dir}/{f}",f"{dst_meshes_dir}/{f}")
        print(f"Successfully copied Mesh files to {dst_meshes_dir}")
    else:
        print(f"ERROR : Unable to find the directory = {root_dir}")

print(f"Found Stretch URDF files at = {root_dir}")
print(f"Robot Model Name = {model_name}")
print(f"Robot Tool Name = {tool_name}")
uncalibrated_urdf_file = f"stretch_description_{model_name}_{tool_name}.urdf"
print(f"URDF to be copied = {uncalibrated_urdf_file}")
make_uncalibrated_urdf(root_dir,uncalibrated_urdf_file)
