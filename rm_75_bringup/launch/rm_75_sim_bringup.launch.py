import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    gazebo = IncludeLaunchDescription(
            os.path.join(
                get_package_share_directory("rm_75_description"),
                "launch",
                "rm_75_gazebo.launch.py"
            )
        )
    
    moveit = IncludeLaunchDescription(
            os.path.join(
                get_package_share_directory("rm_75_moveit_config"),
                "launch",
                "move_group.launch.py"
            ),
        )
    
    return LaunchDescription([
        gazebo,
        moveit,
    ])