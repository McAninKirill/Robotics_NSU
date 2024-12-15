colcon build 
source ./install/setup.bash
ros2 launch robot display_robot.launch.py
rm -rf build install log