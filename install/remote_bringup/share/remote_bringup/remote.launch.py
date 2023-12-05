import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription

def generate_launch_description():
    nav2_pkg_dir = LaunchConfiguration(
        'nav2_pkg_dir',
        default=os.path.join(
            get_package_share_directory('nav2_bringup'))
        )
    
    slam_pkg_dir = LaunchConfiguration(
        'slam_pkg_dir',
        default=os.path.join(
            get_package_share_directory('slam_toolbox'))
        )
    
    explore_pkg_dir = LaunchConfiguration(
        'explore_pkg_dir',
        default=os.path.join(
            get_package_share_directory('explore_lite'))
        )
    
    wait_for_topic = LaunchConfiguration('wait_for_topic')
    return LaunchDescription([
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_pkg_dir, '/launch/navigation_launch.py']),
            
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([slam_pkg_dir, '/launch/online_async_launch.py']),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([explore_pkg_dir, '/launch/explore.launch.py']),
        ),
        Node(
            package='shoe_detector',
            executable='shoe_detect',
            output='screen',
            )

    ])
    
