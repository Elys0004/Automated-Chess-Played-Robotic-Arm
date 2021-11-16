# Robot_driver Description

This is where the vision and the brain of the "gripperone" robotic arm. 

Vision:

We used openCV for its computer vision. In this project, we are not recognizing each of the chess piece individually but instead we used past memory of the chessboard and look into the difference between two frames to identify the chess movement. 
We used the binary image and thresholding to precisely figure out the movement of chess pieces. 

Chess AI algorithm:

For the Chess AI algorithm, we used alpha-beta prunning where it search for the algorithm with the lowest number of nodes by evaluating its min and max, min for its opponent and max for itself. 


Here are the issue and solution that we encountered during this process:

Issue:
