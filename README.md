# Projects at NTU MAE Robotics Club

* Part of an NTU MAERC initiative

## Intermediate Group 3

* Repository for Intermediate Group 3 to build code!

# Automated Chess-played Robotic Arm
## Project Description 
In this project, automated chess-played robotic arm was build to compete and play against human physically so that the player can achieve the real experience even when playing it individually. We decided to go for full-simulation of chess-played robotic arm as a proof of concept which could be potentially being further develop into the real physical chess-played robotic arm. 


Here is the overview of the automated chess-played robotic arm with the chessboard

  <img width="668" alt="Screenshot 2021-11-15 023345" src="https://user-images.githubusercontent.com/90337307/141793068-183b7bc0-cba9-4543-8491-d9807de30003.png">


This automated chess-played robotic arm is build from scratch with the help from various open source contributor. Although we might not be able to achieve the perfect chess-played robotic arm, we hope that this could help others as well. 


Below we will discuss briefly each part of the Chess-played robotic arm. Further details will be discussed inside the folder together with the issue that we encounter that could be improve further. 

1. Environment

   a. gripperone --> gripperone_description 
   
     Our robot is called "gripperone" and in this folder, it contains the meshes and urdf/xacro file of the gripperone robotic arm. This folder also provide a launch file for both in Rviz and Gazebo.
     
     To launch the robot in gazebo, open a new terminal and run the command below
     
     ```
     
     $ roslaunch grippperone_description gazebo.launch
     
     ```
        
     
      
     
     
   b. chess_environment
   
     In this folder, it contains the sdf file of the chessboard. 
     The full environment of the robotic arm and the chessboard can be launch from here as the gripperone robotic arm has been included on the test.launch
     
     ```
     
     $ roslaunch chess_environment test.launch
     
     ```
   
   c. camera
   
      Then the camera plug-in is attached on the gazebo which will be used to detect the player's move. 
      
      Launch a terminal and run the command below to launch the camera
     
     ```
     
      $ rosrun gazebo_ros spawn_model -file ~/catkin_ws/src/camera/camera.urdf -urdf -x 1.18 -y 0 -z 2.5 -R 3.14 -P 1.57 -Y 0 -model camera1
      
     ```
     
      <img width="632" alt="Screenshot 2021-11-15 193049" src="https://user-images.githubusercontent.com/90337307/141797921-faab4fc4-02b0-45d8-ba10-cd422cdb27e4.png">

      The command above will only launch the camera but not capturing it. 
      To able to retrieve the image of the chessboard, launch a new terminal, go to your camera directory and run the command below.
      
     ```
     
      $ python3 image_converter.py
      
     ```
      
      This python script contains a code where it could retrieve and save the image of the current chessboard directly to your robot_driver folder which will be process    further later on. 
      
      Image Retrieved:
      
      <img width="353" alt="Screenshot 2021-11-15 211220" src="https://user-images.githubusercontent.com/90337307/141798097-4b1b3a64-760d-4f3a-a811-083aba09e82c.png">
      <img width="368" alt="Screenshot 2021-11-15 222503" src="https://user-images.githubusercontent.com/90337307/141798305-e91f1c57-bdc0-4dda-9884-77e2032dc935.png">


2.  controller

      We have all the environment set up in the environment folder, this controller will be used to control the movement of the robotic arm. 
      
      <img width="572" alt="Screenshot 2021-11-15 230917" src="https://user-images.githubusercontent.com/90337307/142093714-6f69ac48-63d7-46b6-b206-a5b9a54766e7.png">

      In this controller, we provide two ways on send the commands to the robotic arm:
      
      1. Specifiy the position to each of the joints:
          To enable this, go to ros_controller.launch file under launch folder and make sure it load the "controller.yaml" controller. 
          
         ```
           <rosparam file="$(find GRIP)/config/controllers.yaml" command="load"/>
         
         ```
      2. Send a position for the end-effector:

          To enable this, go to ros_controller.launch file under launch folder and make sure it load the "ros_controllers.yaml" controller. 
          
          ```
           <rosparam file="$(find GRIP)/config/ros_controllers.yaml" command="load"/>
         
          ``` 
       
      In this controller launch file, it could launch the Rviz and Gazebo simultaneously. The Rviz will be beneficial during motion planning and also scripting. 
      
      <img width="664" alt="Screenshot 2021-11-15 230626" src="https://user-images.githubusercontent.com/90337307/141975447-378ff95a-d1e8-43f3-b63c-892278359db5.png">

      To launch this, open new terminal and run the command below:
      
      
          
           $ roslaunch GRIP ros_gazebo.launch
         
           
      
3.  robot_driver

       This is the vision and brain of the "gripperone" robot, where it utilize image processing as it vision to recognize player's move and also chess AI algorithm as it brain to calculate the next best move. 
       
       The output of the chess AI move will then sent to the robotic arm motor driver to move the chess in the desired position. 
       
       <img width="388" alt="Screenshot 2021-11-16 192232" src="https://user-images.githubusercontent.com/90337307/141976765-072be216-f071-434a-90e9-ec28be367042.png">
        
       <img width="389" alt="Screenshot 2021-11-16 192255" src="https://user-images.githubusercontent.com/90337307/141976784-2668c5b4-0598-4308-91e2-563f482fc6fb.png">
       
       In order to run this chess AI script, launch a new terminal and run the command below

          
           $ rosrun robot_driver Chess_AI_ImProc_test.py
         
                  
       
4. grasp_demo.py and gripperone_moveit.py

    This both python script is used to test the movement of the "gripperone" robotic arm controller. 
    
    To run this script, can run the command 
    
          
           $ python3 grasp_demo.py
         
    or       
          
          
           $ python3 gripeerone_moveit.py
         
          



### Steps to clone the repository
* Launch a terminal and run the command  
```
$ git clone https://github.com/ntu-maerc/i3.git 
```



