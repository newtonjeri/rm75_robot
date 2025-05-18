import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory, get_package_prefix

description_pkg = "rm_75_description"
xacro_filename = "rm_75.urdf.xacro"
robot_name = "rm_75"

def generate_launch_description():

    # Path to xacro file
    xacro_file = os.path.join(get_package_share_directory(description_pkg), 'urdf', xacro_filename)
    # model_arg
    model_args = DeclareLaunchArgument(
        name = "model",
        default_value = xacro_file,
        description = "Absolute path to robot urdf"
    )

    # Environment Variable
    os.environ["GAZEBO_MODEL_PATH"] = os.path.join(get_package_prefix(description_pkg), "share")

    # robot_description
    robot_description = ParameterValue(Command(
            ['xacro ', LaunchConfiguration("model")]
        )
    )

    # robot_state_publisher
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}],
        arguments=[xacro_file],
    )

    # gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("gazebo_ros"), "launch", "gazebo.launch.py")
        )
    )
    
    # gazebo spawn entity
    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-entity", robot_name, "-topic", "robot_description"],
        output="screen",
    )

    # Load rm_75_arm controllers
    rm_75_jtc = ExecuteProcess(
        cmd = ["ros2", "control", "load_controller", "--set-state", "active",
                "rm_75_arm_controller"]
    )

    # Load joint state broadcaster
    rm_75_jsbc = ExecuteProcess(
        cmd = ["ros2", "control", "load_controller", "--set-state", "active",
                "joint_state_broadcaster"]
    )


    close_evt1 = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[rm_75_jtc]
        )
    )
    close_evt2 = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=rm_75_jtc,
            on_exit=[rm_75_jsbc]
        )
    )
            
    return LaunchDescription([
        model_args,
        close_evt1,
        close_evt2,
        robot_state_publisher,
        gazebo,
        spawn_entity,
    ])