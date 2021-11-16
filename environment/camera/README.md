# Camera Description

Download and put the camera.urdf somewhere convenient. 

Can be added to already running Gazebo sim using:

  ```
  rosrun gazebo_ros spawn_model -file `pwd`<put the camera.urdf file directory address here> -urdf -x 1.18 -y 0 -z 0.905 -R 3.14 -P 1.57 -Y 0  -model <name of model>
  ```
-x -y -z can be changed to adjust the position of the camera.

After adding the camera to the environment, it will start a topic camera1/image_raw. 
The video can be viewed using the command below:

  ```
  rosrun rqt_image_view rqt_image_view image:=/camera1.
  ```

Rostopic echo will only return a chain of numbers. 

The message type is ROS image. By running the image_converter.py script, it actually convert the ROS Image to OpenCV images and also save the image directly to the robot_driver package so that it can be used further for image processing. 

Here are the issue and solution that we encountered during this process:

Issue:
1. How to send and make the ROS image readable to the robot_driver python script

Solved:
1. We convert with ROS cv_bridge package into OpenCV images and then we save the image using PIL Image module directly to the robot_driver. So image_converter.py script will keep saving the current image that the camera observe and at the mean time, the robot_driver python script will retrieve the image when they need it. 

  ```
   im = Image.fromarray(resize)
   im.save(<robot_drivers/scripts location>)
    
  ```
