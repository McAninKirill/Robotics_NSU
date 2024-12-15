colcon build
source install/setup.bash
gnome-terminal -- bash -c "rqt_robot_steering"
ros2 launch robot_bringup diff_drive.launch.py
rm -rf install log build
