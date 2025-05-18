import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable, LaunchConfiguration

description_pkg = "rm_75_description"
xacro_filename = "rm_75.urdf.xacro"
robot_name = "rm_75"

def generate_launch_description():

    realman_xacro_file = os.path.join(get_package_share_directory(description_pkg), 'urdf',
                                        xacro_filename)
    robot_description = Command(
        [FindExecutable(name='xacro'), ' ', realman_xacro_file])

    return LaunchDescription([
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                name='robot_state_publisher',
                respawn=True,
                parameters=[{'robot_description': robot_description}],
                output='screen'
            ),

            Node(
                package='rviz2',
                executable='rviz2',
                name='rviz2',
                output='screen',
                arguments=['-d', os.path.join(get_package_share_directory(description_pkg), 'rviz', f'{robot_name}.rviz')]
            ),

            Node(
                package='joint_state_publisher_gui',
                executable='joint_state_publisher_gui',
                name='joint_state_publisher_gui',
                output='screen',
            )
        ])
