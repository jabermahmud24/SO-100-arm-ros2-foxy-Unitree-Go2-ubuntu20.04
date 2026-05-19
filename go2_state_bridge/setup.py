from setuptools import setup

package_name = 'go2_state_bridge'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@example.com',
    description='Bridge Go2 lowstate + odom into standard ROS 2 topics',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'state_bridge = go2_state_bridge.state_bridge:main',
        ],
    },
)
