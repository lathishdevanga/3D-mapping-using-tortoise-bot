import os
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.conditions import IfCondition
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, ExecuteProcess

def generate_launch_description():

    # Package name
    package_name='my_robot_gazebo'

    # Launch configurations
    world = LaunchConfiguration('world')

    # Path to default world 
    world_path = "/home/laxmi-arz-i006/lax_bot/src/my_robot_gazebo/worlds/obstacles.world"

    # Launch Arguments
    declare_world = DeclareLaunchArgument(
        name='world', default_value=world_path,
        description='Full path to the world model file to load')
    
    declare_rviz = DeclareLaunchArgument(
        name='rviz', default_value='True',
        description='Opens rviz is set to True')

    # Launch Robot State Publisher Node
    sdf_path = "/home/laxmi-arz-i006/lax_bot/src/my_robot_gazebo/sdf/my_robot.sdf"
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'urdf': sdf_path}.items()
    )

    # Launch the gazebo server to initialize the simulation
    gazebo_server = IncludeLaunchDescription(
                    PythonLaunchDescriptionSource([os.path.join(
                        get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
                    )]), launch_arguments={'gz_args': ['-r -s -v1 ', world], 'on_exit_shutdown': 'true'}.items()
    )

    # Always launch the gazebo client to visualize the simulation
    gazebo_client = IncludeLaunchDescription(
                    PythonLaunchDescriptionSource([os.path.join(
                        get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
                    )]), launch_arguments={'gz_args': '-g '}.items()
    )

    # Run the spawner node from the gazebo_ros package. 
    spawn_entity = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'ros_gz_sim', 'create',
            '-name', 'tortoisebot',
            '-file', sdf_path,
            '-x', '0.0', '-y', '0.0', '-z', '0.2'
        ],
        output='screen'
    )


    static =Node(
                package='tf2_ros',
                executable='static_transform_publisher',
                arguments = ['0', '0', '0', '0', '0', '0', 'base_link', 'tortoisebot/lidar_link/lidar_sensor']
            )



    # Launch the Gazebo-ROS bridge
    bridge_params = "/home/laxmi-arz-i006/lax_bot/src/my_robot_gazebo/config/gz_bridge.yaml"
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',]
    )
    


    # Launch them all!
    return LaunchDescription([
        # Declare launch arguments
        declare_rviz,
        declare_world,

        # Launch the nodes
        rsp,
        gazebo_server,
        gazebo_client,
        ros_gz_bridge,
        spawn_entity,
        static

    ])