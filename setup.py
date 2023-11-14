import setuptools
from os.path import isfile
import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

script_path='./tools'
ex_scripts = glob.glob(script_path+'/*.py') + glob.glob(script_path+'/*.sh')
stretch_scripts=[f for f in ex_scripts if isfile(f)]

setuptools.setup(
    name="hello_robot_stretch_urdf",
    version="0.0.2",
    author="Hello Robot Inc.",
    author_email="support@hello-robot.com",
    description="Stretch URDF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hello-robot/stretch_urdf",
    scripts = stretch_scripts,
    package_data={"": ["*.xacro", "*.STL","*.urdf"]},
    packages=['stretch_urdf'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],

    install_requires=['urdfpy']
)
