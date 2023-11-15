import setuptools
from os.path import isfile
import glob

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="hello_robot_stretch_urdf",
    version="0.0.4",
    author="Hello Robot Inc.",
    author_email="support@hello-robot.com",
    description="Stretch URDF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hello-robot/stretch_urdf",
    package_data={"stretch_urdf": ["RE2V0/meshes/*.STL","RE2V0/urdf/*.xacro","RE2V0/urdf/*.urdf"]},
    packages=['stretch_urdf'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],

    install_requires=['urdfpy']
)
