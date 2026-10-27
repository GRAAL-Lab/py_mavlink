from setuptools import find_packages, setup

package_name = 'py_mavlink'

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
    maintainer='Juri Khanmeh',
    maintainer_email='juri.khanmehn@dfki.de',
    description='Publishing Mavlink messages in ROS topics',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mavlink_publisher = py_mavlink.publisher_mavlink_msg:main',
            'camera_publisher = py_mavlink.camera_image_node:main',
        ],
    },
)
