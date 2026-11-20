from setuptools import find_packages, setup
import os

package_name = 'video_node'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ros2',
    maintainer_email='ros2@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',

    entry_points={
        'console_scripts': [
            'video_node = video_node.video_node:main'
        ],
    },
    
    options={
        'build_scripts':{
            'executable':'/home/ros2/ros2_ws/src/video_node/vide_node/venv_ros2/bin/python3'            
        },
    
    
    },
)
