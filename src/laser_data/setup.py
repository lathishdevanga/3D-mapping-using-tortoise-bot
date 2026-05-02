from setuptools import find_packages, setup

package_name = 'laser_data'

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
    maintainer='laxmi-arz-i006',
    maintainer_email='laxmi-arz-i006@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                "laser = laser_data.laser:main",
                "imu = laser_data.read_data:main",
                "gaz_imu=laser_data.gazebo_imu:main",
        ],
    },
)
