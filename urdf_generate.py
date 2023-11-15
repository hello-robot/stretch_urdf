#!/usr/bin/env python3
import subprocess
import shlex
import sys
import os
from ament_index_python.packages import get_package_share_directory

#Factory tool to generate URDFs from Xacros

def run_cmd(cmdstr):
    process = subprocess.run(shlex.split(cmdstr), capture_output=True, text=True)
    if(process.returncode != 0):
        print("update_uncalibrated_urdf.py ERROR: {}".format(process.stderr), file=sys.stderr)
        sys.exit(1)
    return process

def main():
    root_dir='./stretch_urdf/RE2V0/'
    xacro_dir=root_dir+'xacro/'
    descriptions=['stretch_description_RE2V0_tool_none',
                  'stretch_description_RE2V0_tool_stretch_gripper',
                  'stretch_description_RE2V0_tool_dex_wrist']
    urdfs=[]
    for d in descriptions:
        bashCommand = "ros2 run xacro xacro {}".format(xacro_dir+d+'.xacro')
        print(bashCommand)
        process = run_cmd(bashCommand)
        urdf = process.stdout
        urdf_filepath = root_dir+d+'.urdf'
        urdfs.append(urdf_filepath)
        urdf_lines=urdf.split('\n')
        with open(urdf_filepath, "w") as open_file:
            for u in urdf_lines:
                if u.find('d435.dae')>-1: #Replace path for realsense
                    ss=u.find('file://')
                    u = u[:ss] + './meshes/d435.dae"/>'
                print(u, file=open_file)

            open_file.close()


if __name__ == '__main__':
     main()
