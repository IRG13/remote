import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node, WaitForMessage
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription

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
        WaitForMessage(
            condition=LaunchConfiguration('wait_for_message'),
            topic='bot_started',  # Replace with the actual topic you want to wait for
            timeout=60.0,  # Adjust the timeout as needed
            output='screen',
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