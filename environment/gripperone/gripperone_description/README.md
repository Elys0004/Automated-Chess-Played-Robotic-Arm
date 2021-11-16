# Gripperone Description

Our "gripperone" robotic arm is designed and assembled using Fusion360. By installing an open source adds-in, "fusion2urdf" plugin, we manage to succesfully convert the 3D model to urdf-xacro file.



Here are the issue and solution that we encountered during this process:
Issue:
1. Process of converting the 3D model to urdf file. 
2. The robot base_link is not attached to the ground and the error state that it does not support root link with an inertia


Solved:
1. Need to make sure that all parts of the assembly come from a single body instead of component. Make sure to read the "fusion2urdf" documention carefully.
2. Create dummy link and virtual joint using the command below:
     ```
     
     <link name= "world"/>

      <joint name="fixed" type = "fixed">
	        <parent link ="world"/>
	        <child link ="base_link"/>
      </joint>
      
     ```
