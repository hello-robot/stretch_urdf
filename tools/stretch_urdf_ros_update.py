#!/usr/bin/env python3

import os
import sys
from stretch_body.robot_params import RobotParams
import subprocess
import shlex
import re
import stretch_body.hello_utils as hu

root_dir = None
tool_name = RobotParams().get_params()[1]['robot']['tool']
model_name = RobotParams().get_params()[1]['robot']['model_name']


def run_cmd(cmdstr,verbose=False):
    if verbose:
        print(cmdstr)
    process = subprocess.run(shlex.split(cmdstr), capture_output=True, text=True)
    if(process.returncode != 0):
        print("ERROR: {}".format(process.stderr), file=sys.stderr)
        sys.exit(1)
    return process

def remove_lines_between_patterns(text, start_pattern, end_pattern):
    start_regex = re.compile(re.escape(start_pattern) + r'.*?' + re.escape(end_pattern), re.DOTALL)
    end_regex = re.compile(re.escape(end_pattern) + r'.*?' + re.escape(start_pattern), re.DOTALL)
    cleaned_text = start_regex.sub(start_pattern + end_pattern, text)
    cleaned_text = end_regex.sub(start_pattern + end_pattern, cleaned_text)
    cleaned_text = cleaned_text.replace(start_pattern + end_pattern, "")
    return cleaned_text

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

if ros_version==2:
    ros_repo_path = '/home/hello-robot/ament_ws/src/stretch_ros2'
else:
    ros_repo_path = f'/home/hello-robot/catkin_ws/src/stretch_ros'

print(f"Found Stretch URDF files at = {root_dir}")
print(f"Robot Model Name = {model_name}")
print(f"Robot Tool Name = {tool_name}")
data_dir = f"{root_dir}/{model_name}"
print(f"Data Directory = {data_dir}")

def search_and_replace(file_path, search_word, replace_word):
   with open(file_path, 'r') as file:
      file_contents = file.read()

      updated_contents = file_contents.replace(search_word, replace_word)

   with open(file_path, 'w') as file:
      file.write(updated_contents)

def copy_mesh_files():
    for f in os.listdir(f"{data_dir}/meshes/"):
        src = f"{data_dir}/meshes/{f}"
        dst = f"{ros_repo_path}/stretch_description/meshes/"
        cmd = f"cp -r {src} {dst}"
        print(cmd)
        os.system(cmd)
        
stretch_description_xacro = f"stretch_description_{model_name}_{tool_name}.xacro"
def copy_xacro_files():
    # Process and copy the xacro files to ros
    for f in os.listdir(f"{data_dir}/xacro/"):
        src = f"{data_dir}/xacro/{f}"
        dst = f"{ros_repo_path}/stretch_description/urdf/"
        cmd = f"cp -r {src} {dst}"
        print(cmd)
        os.system(cmd)

        # Replace meshses path to point to ros package source
        try:
            search_and_replace(f"{dst}/{f}",'./meshes','package://stretch_description/meshes')
        except IsADirectoryError:
            for f2 in os.listdir(f"{dst}/{f}"):
                search_and_replace(f"{dst}/{f}/{f2}",'./meshes','package://stretch_description/meshes')
        
        # Manually remove the link_ground and joint_ground
        if f == 'stretch_main.xacro':
            main = f"{dst}/{f}"
            file = open(main)
            r = remove_lines_between_patterns(file.read(),'<link\n    name="link_ground">','</link>')
            r = remove_lines_between_patterns(r,'<joint\n    name="joint_ground"','</joint>')
            file.close()
            os.system(f"rm {main}")
            f = open(main, "a")
            f.write(r)
            f.close()


print("\nCopying Mesh Files.......\n")
copy_mesh_files()
print("\nCopying Xacro Files.......\n")
copy_xacro_files()

print("\nUpdate stretch_description.xacro.......\n")
if stretch_description_xacro in os.listdir(f"{ros_repo_path}/stretch_description/urdf/"):
    cmd = f"cp {ros_repo_path}/stretch_description/urdf/{stretch_description_xacro} {ros_repo_path}/stretch_description/urdf/stretch_description.xacro"
    print(cmd)
    os.system(cmd)