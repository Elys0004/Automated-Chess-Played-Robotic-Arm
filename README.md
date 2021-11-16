# Projects at NTU MAE Robotics Club

* Part of an NTU MAERC initiative

## Intermediate Group 3

* Repository for Intermediate Group 3 to build code!

# Chess-played Robotic Arm
## Project Description 
In this project, chess-played robotic arm was build to compete and play against human physically so that the player can achieve the real experience even when playing it individually. We decided to go for full-simulation of chess-played robotic arm as a proof of concept which could be potentially being further develop into the real physical chess-played robotic arm. 


Here is the overview of the chess-played robotic arm with the chessboard

  <img width="668" alt="Screenshot 2021-11-15 023345" src="https://user-images.githubusercontent.com/90337307/141793068-183b7bc0-cba9-4543-8491-d9807de30003.png">


The robot is build from scratch and it is made possible thank you to the combination and help of various open source contributor. Although we might not be able to achieve the perfect chess-played robotic arm, we hope that this could help others as well. 


Below we will discuss briefly each part of the Chess-played robotic arm. Further details will be discussed inside the folder together with the issue that we encounter that could be improve further. 
1. Environment
   a. gripperone --> gripperone_description 
   
     Our robot is called "gripperone" and in this folder, it contains the urdf/xacro file of the gripperone robotic arm.
     
   b. chess_environment
     In this folder, it contains the sdf file of the chessboard. 
     The full environment of the robotic arm and the chessboard can be launch from here as the gripperone robotic arm has been included on the test.launch
     
     ```
     
     $ roslaunch chess_environment test.launch
     
     ```
   
   c. camera
      Then the camera plug-in is attached on the gazebo which will be used to capture the movement of the chess on the chessboard. 
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

---
In this state

2.  


### Steps to clone the repository
* Launch a terminal and run the command  
```
$ git clone https://github.com/ntu-maerc/i3.git 
```



