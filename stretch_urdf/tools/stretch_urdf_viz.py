#!/usr/bin/env python3
import argparse
import math
import yaml
import pathlib
import urchin as urdf_loader
import pyrender
import warnings
import glob

from hello_helpers.gripper_conversion import GripperConversion
import stretch_body.robot
import stretch_body.device
import stretch_body.hello_utils as hu
import importlib.resources as importlib_resources

hu.print_stretch_re_use()
warnings.filterwarnings("ignore")

class URDFVisualizer:
    """The `show` method in this class is modified from the
    original implementation of `urdf_loader.URDF.show`. This class
    exists temporarily while the PR for this modification is
    in review.
    """

    def __init__(self, urdf):
        self.urdf = urdf
        self.nodes = None
        self.scene = None
        self.viewer = None

    def show(self, cfg=None, use_collision=False):
        """Visualize the URDF in a given configuration.
        Parameters
        ----------
        cfg : dict or (n), float
            A map from joints or joint names to configuration values for
            each joint, or a list containing a value for each actuated joint
            in sorted order from the base link.
            If not specified, all joints are assumed to be in their default
            configurations.
        use_collision : bool
            If True, the collision geometry is visualized instead of
            the visual geometry.
        """
        if use_collision:
            fk = self.urdf.collision_trimesh_fk(cfg=cfg)
        else:
            fk = self.urdf.visual_trimesh_fk(cfg=cfg)

        self.scene = pyrender.Scene()
        self.nodes = []
        for tm in fk:
            pose = fk[tm]
            mesh = pyrender.Mesh.from_trimesh(tm, smooth=False)
            mesh_node = self.scene.add(mesh, pose=pose)
            self.nodes.append(mesh_node)
        self.viewer = pyrender.Viewer(self.scene, run_in_thread=True, use_raymond_lighting=True)

    def update_pose(self, cfg=None, use_collision=False):
        if use_collision:
            fk = self.urdf.collision_trimesh_fk(cfg=cfg)
        else:
            fk = self.urdf.visual_trimesh_fk(cfg=cfg)

        self.viewer.render_lock.acquire()
        for i, tm in enumerate(fk):
            pose = fk[tm]
            self.scene.set_pose(self.nodes[i], pose=pose)
        self.viewer.render_lock.release()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Python based URDF visualization')
    parser.add_argument('-t', "--trajectory", help="Visualize predefined trajectory", action="store_true")
    parser.add_argument('-c', "--collision", help="Use collision meshes", action="store_true")
    args = parser.parse_args()

    pkg = str(importlib_resources.files("stretch_urdf"))  # .local/lib/python3.10/site-packages/stretch_urdf)
    models=['RE1V0','RE2V0','SE3']
    urdf_files=[]
    for m in models:
        urdf_files=urdf_files+glob.glob(pkg+'/'+m+'/*.urdf')
    print('-------------------')
    for i in range(len(urdf_files)):
        a=urdf_files[i]
        fn=a[a.find('stretch_description'):]
        print('%d : %s'%(i,fn))
    print('-------------------')
    id=0
    while True:
        id=int(input('Enter ID of URDF to viz: '))

        if id>=0 and id<len(urdf_files):
            break
        print('Invalid entry')
    urdf_name=urdf_files[id]

    urdf = urdf_loader.URDF.load(urdf_name)
    tool = stretch_body.device.Device(req_params=False).robot_params['robot']['tool']
    viz = URDFVisualizer(urdf)


    if args.trajectory:
        cfg_trajectory = {
            'joint_left_wheel': [0.0, math.pi],
            'joint_right_wheel': [0.0, math.pi],
            'joint_lift': [0.9, 0.7],
            'joint_arm_l0': [0.0, 0.1],
            'joint_arm_l1': [0.0, 0.1],
            'joint_arm_l2': [0.0, 0.1],
            'joint_arm_l3': [0.0, 0.1],
            'joint_wrist_yaw': [math.pi, 0.0],
            #'joint_gripper_finger_left': [0.0, 0.25],
            #'joint_gripper_finger_right': [0.0, 0.25],
            'joint_head_pan': [0.0, -(math.pi / 2.0)],
            'joint_head_tilt': [0.5, -0.5]
        }
        # if tool == 'tool_stretch_dex_wrist':
        #     cfg_trajectory['joint_wrist_pitch'] = [-math.pi/2, 0.0]
        #     cfg_trajectory['joint_wrist_roll'] = [-math.pi, 0.0]
        urdf.animate(cfg_trajectory=cfg_trajectory, use_collision=args.collision)
    else:
        cfg_pose = {
            'joint_left_wheel': 0.0,
            'joint_right_wheel': 0.0,
            'joint_lift': 0.6,
            'joint_arm_l0': 0.1,
            'joint_arm_l1': 0.1,
            'joint_arm_l2': 0.1,
            'joint_arm_l3': 0.1,
            'joint_wrist_yaw': math.pi,
            #'joint_gripper_finger_left': 0.0,
            #'joint_gripper_finger_right': 0.0,
            'joint_head_pan': -(math.pi / 2.0),
            'joint_head_tilt': -0.5
        }
        # if tool == 'tool_stretch_dex_wrist':
        #     cfg_pose['joint_wrist_pitch'] = -math.pi/2
        #     cfg_pose['joint_wrist_roll'] = math.pi/4
        urdf.show(cfg=cfg_pose, use_collision=args.collision)



