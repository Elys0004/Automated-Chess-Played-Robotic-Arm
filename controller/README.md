# Controller Description

This is the controller that is used to control the "gripperone" robotic arm. We used the MoveIt package for manipulation. This MoveIt package consists of controllers and a package manager. 

In this package, it integrates Rviz and Gazebo where Rviz is used for its motion planning and Gazebo is used to show the executed move.


<img width="584" alt="Screenshot 2021-11-15 230749" src="https://user-images.githubusercontent.com/90337307/142190731-ba97849e-e78a-4470-b5cd-a84ce3af2c16.png">

There are two ways of controlling the robotic arm:

i. Specifying the position of each joint. 

 To load this controller, "controller.yaml" is loaded inside the the "ros_controllers.launch" where it consists of joint position command for each of the joint.
 
 The joint position can be specified by using python script or launching a new terminal, and run the command below:
 
  ```
  $ rostopic pub -1 <your joint position controller topic> /command std_msgs/Float64 "data: <the rotation position of the joint>"
  ```
  For "gripperone" robotic arm, you can replace <your joint position controller> with one of the 7 joint of the robot for example 
  
  ```
  $ rostopic pub -1 /gripperone/joint2_position_controller /command std_msgs/Float64 "data: -1"
  ``` 
  
ii. Send a position for the end effector
  
   To load this controller, "ros_controller.yaml" is loaded inside the the "ros_controllers.launch" where it consists of two groups, arm controller and hand controller. The motion can be planned through Rviz or python script. 
  
  
Here are the issue and solution that we encountered during this process:

Issue:
  
1. The moveit package joint does not rotate in the desired rotation during creating the moveit package.
  
2. The robotic arm doesn't want to move

3. Gazebo cannot recognize and publish the arm and hand controller topic.
  
Partially solved:
  
 1. Make sure when designing the robotic arm, the joint name is not double and every joint link is assembly well. Then regenerate the urdf file.
 
 2. The robotic arm cannot move because need to do some tuning on the PID controller. We use rqt_gui interface to know the parameter suitable for the PID controller on each joint.
  
  <img width="685" alt="Screenshot 2021-11-17 195349" src="https://user-images.githubusercontent.com/90337307/142196177-9a6b34cc-e00c-48be-9943-c37bf19ae780.png">
  
  As shown in the picture above, tune the PID so that the graph between the command given to the joint (blue) and the joint state value (red) should roughly shows the same sinusoidal function. The joint state value shows the current position of the joint that you specified as shown in the gazebo as well. 
 
  To run the rqt gui, open new launch terminal and run the command below:
  
  ``` 
  rosrun rqt_gui rqt_gui
  
  ```
  
  Although we can successfully move each joint to a desired place, but the joint is not well controlled yet and it might be because of the PID controller since it depends on another controller and we have 7 joint controller that could effect each other. 
  
 3. Although the MoveIt package could be generated using MoveIt setup assistant, there is some part that need to add on in order to make the controller works. 
  
  On ros_controllers.launch file, we add our controller inside the args, as shown below:
  
  ```
  <node name="controller_spawner" pkg="controller_manager" type="spawner" respawn="false"
    output="screen" ns="/gripperone" args="--namespace=/gripperone
    					  joint_state_controller
					  arm_controller
					  hand_controller"/>
  ```
  
  Not only that, we also add joint trajectory controller for each group controller (arm and hand) in the "ros_controller.yaml" file.
  
  ```
   arm_controller:
    type: effort_controllers/JointTrajectoryController
    joints:
        - Rev1
        - Rev2
        - Rev3
        - Rev4
    gains:
        Rev1: { p: 2000, d: 50, i: 0.01, i_clamp: 10000 }
        Rev2: { p: 2000, d: 100, i: 0.01, i_clamp: 10000 }
        Rev3: { p: 2000, d: 50, i: 0.01, i_clamp: 1 }
        Rev4: { p: 2000, d: 70, i: 0.01, i_clamp: 10000 }

    constraints:
        goal_time: 10.0
    state_publish_rate: 25

  hand_controller:
    type: effort_controllers/JointTrajectoryController
    joints:
        - Rev5
        - Rev6
        - Rev7

    gains:
        Rev5: { p: 1000, d: 3.0, i: 0, i_clamp: 1 }
        Rev6: { p: 1000, d: 1.0, i: 0, i_clamp: 1 }
        Rev7: { p: 1000, d: 1.0, i: 0, i_clamp: 1 }

    state_publish_rate: 25
   
  ```
Now we have actually successfully publish the group topic. However, there is still and issue where when we try to move the robot arm on gazebo, it stated that the controller list is zero. We are quite sure that the controller are actually exist through troubleshooting step shown in this video -->  https://www.youtube.com/watch?v=P7I0n1RPRuk Hence, we can plan on the Rviz but when we try to execute the robot on Rviz, it will show that it failed. 
