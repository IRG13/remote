import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition
def generate_launch_description():
    nav2_pkg_dir = LaunchConfiguration(
        'nav2_pkg_dir',
        default=os.path.join(
            get_package_share_directory('nav2_bringup'), 'launch')
        )
    
    slam_pkg_dir = LaunchConfiguration(
        'slam_pkg_dir',
        default=os.path.join(
            get_package_share_directory('slam_toolbox'), 'launch')
        )
    
    explore_pkg_dir = LaunchConfiguration(
        'explore_pkg_dir',
        default=os.path.join(
            get_package_share_directory('explore_lite'), 'explore/launch')
        )
    
    return LaunchDescription([
        DeclareLaunchArgument('wait_for_topic', default_value='false', description='Set to true to wait for the topic'),

        # Custom Python script to wait for a specific message on a topic
        Node(
            package='remote-bringup',
            executable='waiter',  # Create a Python script for waiting
            output='screen',
            arguments=[('--wait_for_topic', LaunchConfiguration('wait_for_topic'))],
            condition=IfCondition('launch.configurations["wait_for_topic"].value == "true"'),
        ),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_pkg_dir, 'navigation_launch.py'])
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([slam_pkg_dir, 'online_async_launch.py'])
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([explore_pkg_dir, 'explore.launch.py'])
        ),
        Node(
            package='shoe_detector',
            executable='shoe_detect',
            output='screen',
        )

    ])
    
