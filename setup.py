from setuptools import setup

package_name = 'gesture_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools', 'opencv-python', 'mediapipe'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='Hand gesture controlled TurtleBot using OpenCV and Mediapipe',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gesture_control = gesture_controller.gesture_control:main',
        ],
    },
)

