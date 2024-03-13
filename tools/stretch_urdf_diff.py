from stretch_body.robot_params import RobotParams
import urchin

def compare_urdfs(urdf1_file, urdf2_file):
    # Load URDF files
    model1 = urchin.URDF.load(urdf1_file)
    model2 = urchin.URDF.load(urdf2_file)

    # Get lists of links and joints
    links1 = model1.get_links()
    links2 = model2.get_links()
    joints1 = model1.get_joints()
    joints2 = model2.get_joints()

    # Compare links
    print("Changes in links:")
    for link_name in links1:
        if link_name in links2:
            link1 = model1.get_link(link_name)
            link2 = model2.get_link(link_name)
            if link1 != link2:
                print(f"Link '{link_name}' has changed:")
                print(f"  - In URDF1: {link1}")
                print(f"  - In URDF2: {link2}")
        else:
            print(f"Link '{link_name}' is missing in URDF2")

    # Compare joints
    print("\nChanges in joints:")
    for joint_name in joints1:
        if joint_name in joints2:
            joint1 = model1.get_joint(joint_name)
            joint2 = model2.get_joint(joint_name)
            if joint1 != joint2:
                print(f"Joint '{joint_name}' has changed:")
                print(f"  - In URDF1: {joint1}")
                print(f"  - In URDF2: {joint2}")
        else:
            print(f"Joint '{joint_name}' is missing in URDF2")

if __name__ == "__main__":
    urdf1_file = "/home/hello-robot/repos/stretch_urdf/stretch_urdf/SE3/stretch_description_SE3_eoa_wrist_dw3_tool_sg3.urdf"
    urdf2_file = "path/to/second.urdf"
    compare_urdfs(urdf1_file, urdf2_file)
