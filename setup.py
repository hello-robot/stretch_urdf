import setuptools
from os.path import isfile
import glob

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="hello_robot_stretch_urdf",
    version="0.0.13",
    author="Hello Robot Inc.",
    author_email="support@hello-robot.com",
    description="Stretch URDF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hello-robot/stretch_urdf",
    package_data={"stretch_urdf": ["RE2V0/meshes/*.STL","RE2V0/meshes/*.dae","RE2V0/*.urdf"]},
    packages=['stretch_urdf'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],

    install_requires=['urchin']
)
