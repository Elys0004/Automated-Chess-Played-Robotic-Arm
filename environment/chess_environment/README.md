# Chess_environment Description

After obtaining the chess-pieces dae file from open-source contributors, we create a sdf file to define the world environment into the Gazebo simulation. 

We have also integrated the "gripperone" robot with the chess environment in "test.laucnh" so that it could be launch together in one launch file. 

Here are the issue and solution that we encountered during this process:

Issue:
1. All the chess pieces are falling down as there is no ground in the gazebo.
2. The chess pieces is all floating around.


Solved:
1. Need to add ground plane in the world file. 
    
    ```
    <include>
  	  <uri>model://ground_plane</uri>
  	</include>
    
    ```
    
2. This is because the inertia is not properly set up. We use mesh lab to calculate the inertia for the chess pieces. 

    <img width="894" alt="Screenshot 2021-11-16 185612" src="https://user-images.githubusercontent.com/90337307/141986008-5c023a50-2aca-43a6-ae22-758bbf7c9c5a.png">

   Although after tuning the inertia, it improves a lot and the chess piece are all sit in the ground quite well, it still a little bit wobbly for some of the chess pieces. 
   It might be due to the fact that we used the same inertia to represent all the chess pieces. All the chess pieces have different height and diameter, it is best option to find each of the chess pieces inertia for better stability. 
