from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command


def generate_launch_description():

    # Package name
    package_name = FindPackageShare("diff_drive_robot")

    # Default robot description if none is specified
    sdf_path = "/home/laxmi-arz-i006/lax_bot/src/my_robot_gazebo/sdf/my_robot.sdf"
    
    # Launch configurations
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Declare launch arguments
    declare_use_sim_time = DeclareLaunchArgument(
            'use_sim_time', default_value='false',
            description='Use sim time if true')

    declare_urdf = DeclareLaunchArgument(
            name='sdf', default_value=sdf_path,
            description='Path to the robot description file')

    # Create a robot state publisher 
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time,'robot_description':open(sdf_path).read() ,}],
    )

    # Launch!
    return LaunchDescription([
        declare_urdf,
        declare_use_sim_time,
        robot_state_publisher
    ])