from setuptools import setup

package_name = 'follower_arm_driver'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='unitree',
    maintainer_email='unitree@todo.todo',
    description='Simple Foxy Serial bridge for follower arm',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'arm_bridge = follower_arm_driver.arm_bridge:main',
        ],
    },
)
