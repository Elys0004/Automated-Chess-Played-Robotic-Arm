#!/usr/bin/env python
# coding: utf-8

# # Code for Image Processing and Chess AI in Python
# 
# Image Processing using OpenCV and the implementation of AI uses the Minimax algorithm
# 
# Module used:
# 
# - `Python Chess` : `pip install python-chess`
# - `Main modules packages: Opencv` : `pip install opencv-python` 
# - `Full package`: `pip install opencv-contrib-python`
# - `Numpy`: `pip install numpy`
# 

# In[1]:


import chess
board = chess.Board()
board
import rospy
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image as ImageMsg
from PIL import Image

# ### Initialize the movement table for each piece

# In[2]:


# The tables denote the points scored for the position of the chess pieces on the board.

pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]
bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]
rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]
queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]
kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


# In[3]:


# sReturn the heuristic of the 
def eval_board():
    
    # Note that I have no experience in chess so don't ask me how tf I got this
    
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0
    
    # Calculate the no of pieces
    white_pawn = len(board.pieces(chess.PAWN, chess.WHITE))
    nigga_pawn = len(board.pieces(chess.PAWN, chess.BLACK))
    white_knight = len(board.pieces(chess.KNIGHT, chess.WHITE))
    nigga_knight = len(board.pieces(chess.KNIGHT, chess.BLACK))
    white_bishop = len(board.pieces(chess.BISHOP, chess.WHITE))
    nigga_bishop = len(board.pieces(chess.BISHOP, chess.BLACK))
    white_rook = len(board.pieces(chess.ROOK, chess.WHITE))
    nigga_rook = len(board.pieces(chess.ROOK, chess.BLACK))
    white_queen = len(board.pieces(chess.QUEEN, chess.WHITE))
    nigga_queen = len(board.pieces(chess.QUEEN, chess.BLACK))
    
    
    material = 100 * (white_pawn - nigga_pawn) + 320 * (white_knight - nigga_knight) + 330 * (white_bishop - nigga_bishop) + 500 * (white_rook - nigga_rook) + 900 * (white_queen - nigga_queen)
    
    
    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])
    
    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    
    if board.turn:
        return eval
    else:
        return -eval
    


# In[4]:


def move_pieces(depth):
    import chess.polyglot
    try:
        move = chess.polyglot.MemoryMappedReader("/home/elysia/catkin_ws/src/robot_driver/scripts/Opening_Moves/pecg_book.bin").weighted_choice(board).move
#         move = chess.polyglot.MemoryMappedReader("C:/Users/Justin/Documents/Projects/Chess/Opening_Moves/human.bin").weighted_choice(board).move
#         move = chess.polyglot.MemoryMappedReader("C:/Users/Justin/Documents/Projects/Chess/Opening_Moves/computer.bin").weighted_choice(board).move

        return move
    
    except:
        bestMove = chess.Move.null()
        alpha = - 100000
        beta = 100000
        bestValue = -99999
        
        for move in board.legal_moves:
            board.push(move)
            boardValue = -alphabetapruning(-beta, -alpha, depth - 1)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if (boardValue > alpha):
                alpha = boardValue
            board.pop()
        return bestMove


# In[5]:


def alphabetapruning(alpha, beta, depth):
    
    bestScore = -9999
    if (depth == 0):
        return quiesce(alpha, beta)

    for move in board.legal_moves:
        board.push(move)
        score = -alphabetapruning(-beta, -alpha, depth - 1)
        board.pop()
        if (score >= beta):
            return score
        if (score > bestScore):
            bestscore = score
        if (score > alpha):
            alpha = score
    return bestscore
    


# In[6]:


def quiesce(alpha, beta):
    stand_pat = eval_board()
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(-beta, -alpha)
            board.pop()

            if (score >= beta):
                return beta
            if (score > alpha):
                alpha = score
    return alpha


# In[7]:


def chessboard(image):
    x = 0
    y = 0
    points = np.zeros((9,9,2))
    for i in range(9):
        for j in range(9):
            x = i * 100
            y = j * 100
            points[i][j][0] = x
            points[i][j][1] = y
    boxes = np.zeros((9,9,4))
    for i in range(8):
        for j in range(8):  
            boxes[i][j][0] = points[i][j][0]
            boxes[i][j][1] = points[i][j][1]
            boxes[i][j][2] = points[i+1][j+1][0]
            boxes[i][j][3] = points[i+1][j+1][1]
    for i in range(8):
        for j in range(8):
            box1= boxes [i,j]
            cv2.rectangle(image, (int(box1[0]),int(box1[1])),(int(box1[2]),int(box1[3])), (255,0,0), 2)
            cv2.putText(image,"({},{})".format(i,j),(int(box1[2])-70, int(box1[3])-50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
    return boxes, points


# In[8]:


def contour(image,imagemove):    
    image_diff = cv2.absdiff(image,imagemove)
    image_diff_gray = cv2.cvtColor(image_diff,cv2.COLOR_BGR2GRAY)
    matrix,threshold=  cv2.threshold(image_diff_gray,10,255,cv2.THRESH_BINARY) #turn into binary image (become 255 and 0)
    cntrs,hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #find the counter of each part that have different contrast(the binary that have been made with the threshold)
    return cntrs, hierarchy, image_diff


# In[9]:


def chessmove_mid(cntrs,image_diff):
    if len(cntrs) >= 2:
        required_contoures_mid_point = []
        for c in cntrs:
            area = cv2.contourArea(c)
            if area> 500:
                (x, y, w, h) = cv2.boundingRect(c)
                required_contoures_mid_point.append([x+int(w/2),y+int(h/2)])
                cv2.rectangle(image_diff, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return required_contoures_mid_point
    


# In[10]:


def board_reset():
    fen_line = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    chess_board = []
    current_player_bool_position = []
    for row in fen_line.split(' ')[0].split('/'):
        bool_row = []
        chess_row = []
        for cell in list(row):
            if cell.isnumeric():
                for i in range(int(cell)):
                    chess_row.append(str(1))
                    bool_row.append(0)
            else:
                chess_row.append(cell)
                bool_row.append(1)
        chess_board.append(chess_row)
        current_player_bool_position.append(bool_row)
    chessposition = np.array(chess_board)
    current_player_bool_position = np.array(current_player_bool_position)
    return chessposition, current_player_bool_position


# In[11]:


def fenboard(fen_line):
    chess_board = []
    current_player_bool_position = []
    for row in fen_line.split(' ')[0].split('/'):
        bool_row = []
        chess_row = []
        for cell in list(row):
            if cell.isnumeric():
                for i in range(int(cell)):
                    chess_row.append(str(1))
                    bool_row.append(0)
            else:
                chess_row.append(cell)
                bool_row.append(1)
        chess_board.append(chess_row)
        current_player_bool_position.append(bool_row)
    chessposition = np.array(chess_board)
    current_player_bool_position = np.array(current_player_bool_position)
    return chessposition, current_player_bool_position
    


# In[12]:


def movement(chessposition, key1, key2,x,y,x1,y1):
    movement = 0
    
    for i in "RNQKBP": 
            if chessposition[y,x] == '1' and movement ==0:
                print(key2, "move to", key1)
                movement = 1
                a = chessposition[y1,x1]
                b = key1
                chessposition[y1,x1]= chessposition[y,x]
                chessposition[y,x] = a
            elif chessposition[y1,x1] == i:
                print(key1, "eating",key2)
                movement = 1
                a = chessposition[y,x]
                b = key2
                chessposition[y1,x1]= chessposition[y,x]
                chessposition[y,x] = 1
            elif chessposition[y,x] == i:
                print(key2, "eating", key1)
                movement = 1
                a = chessposition[y1,x1]
                b = key1
                chessposition[y,x]= chessposition[y1,x1]
                chessposition[y1,x1] = 1
    if movement == 0:
        print(key1, "move to",key2)
        a = chessposition[y,x]
        b = key2
        chessposition[y,x]= chessposition[y1,x1]
        chessposition[y1,x1] = a
    return a,b


# In[13]:


def get_key(val):
    map_position = {}
    x,y = 0,0
    for i in "abcdefgh":
        for j in "87654321":
            map_position[i+j]= [x,y]
            y = (y+1)%8
        x = (x+1)%8
    for key, value in map_position.items():
            if val[0] == value:
                key1 = key
    for key, value in map_position.items():
            if val[1] == value:
                key2 = key
                return key1,key2
    return "key doesn't exist"


# In[14]:


def midrange(midpoint,points):	
    for j in range(8):
                if points[1][j][1]  < midpoint[0][1] < points[1][j+1][1]:
                    yleft = points[1][j][1]
                    yright= points[1][j+1][1]
    for i in range(8):
                if points[i][1][0]< midpoint[0][0] < points[i+1][1][0]:
                    xleft = points[i][1][0]
                    xright = points[i+1][1][0]
                    
    for j in range(8):
                if points[1][j][1] < midpoint[1][1] < points[1][j+1][1]:
                    y1left = points[1][j][1]
                    y1right= points[1][j+1][1]
    for i in range(8):
                if points[i][1][0] < midpoint[1][0] < points[i+1][1][0]:
                    x1left = points[i][1][0]
                    x1right = points[i+1][1][0]
    return yleft, yright, xleft, xright, y1left, y1right, x1left, x1right 


# In[15]:


def which_box(boxes,yleft, yright, xleft, xright, y1left, y1right, x1left, x1right):
    val = []
    for i in range(8):
        for j in range(8): 
            if xleft == boxes[i][j][0] and xright == boxes[i][j][2] and yleft == boxes[i][j][1] and yright == boxes[i][j][3]:
                x = i
                y = j
                val.append([x,y])
            
    for i in range(8):
        for j in range(8): 
            if x1left == boxes[i][j][0] and x1right == boxes[i][j][2] and y1left == boxes[i][j][1] and y1right == boxes[i][j][3]:
                x1 = i
                y1 = j
                val.append([x1,y1])
            
    return val,x,y,x1,y1


# In[16]:


def output(a,b):
    if a == "p":
        a = ''
    return a+b


# In[17]:


def get_val(keyop):
    map_position = {}
    x,y = 0,0
    for i in "abcdefgh":
        for j in "87654321":
            map_position[i+j]= [x,y]
            y = (y+1)%8
        x = (x+1)%8
    for key, value in map_position.items():
            if keyop == key:
                return value
    return "key doesn't exist"




def movementop(chessposition, key1, key2,x,y,x1,y1):
    movement = 0
    
    for i in "rnqkbp": 
            if chessposition[y,x] == '1' and movement ==0:
                print(key2, "move to", key1)
                movement = 1
                a = chessposition[y1,x1]
                b = key1
                chessposition[y1,x1]= chessposition[y,x]
                chessposition[y,x] = a
            elif chessposition[y1,x1] == i:
                print(key1, "eating",key2)
                movement = 1
                a = chessposition[y,x]
                b = key2
                chessposition[y1,x1]= chessposition[y,x]
                chessposition[y,x] = 1
            elif chessposition[y,x] == i:
                print(key2, "eating", key1)
                movement = 1
                a = chessposition[y1,x1]
                b = key1
                chessposition[y,x]= chessposition[y1,x1]
                chessposition[y1,x1] = 1
    if movement == 0:
        print(key1, "move to",key2)
        a = chessposition[y,x]
        b = key2
        chessposition[y,x]= chessposition[y1,x1]
        chessposition[y1,x1] = a
    return a,b
    
def talker(final):
    pub = rospy.Publisher('movement', String, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    a = 0
    pub.publish(final)
    rate.sleep()	
   	
class image_convertermove:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera1/image_raw",ImageMsg,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "rgb8")
    except CvBridgeError as e:
      print(e)
    print(cv_image)
    crop_image = cv_image[260:540,260:540]
    cv2.imshow('test', crop_image)
    resize = cv2.resize(crop_image,(800,800))
    print(resize.shape)
    im = Image.fromarray(resize)
    im.save(r'/home/elysia/catkin_ws/src/robot_driver/scripts/chessmove.png')
    cv2.waitKey(0)
    cv2.imwrite('image.jpg',crop_image)  
    
class image_converter:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera1/image_raw",ImageMsg,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "rgb8")
    except CvBridgeError as e:
      print(e)
    print(cv_image)
    crop_image = cv_image[260:540,260:540]
    resize = cv2.resize(crop_image,(800,800))
    cv2.imshow('test', resize)
    print(resize.shape)
    im = Image.fromarray(resize)
    im.save(r'/home/elysia/catkin_ws/src/robot_driver/scripts/chess.png')
    cv2.waitKey(0)
    rospy.signal_shutdown('Bye')
    
# # Start
# 

# In[27]:


import chess.svg
import chess.pgn
import chess.engine
from IPython.display import SVG
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt


# In[33]:


board


# In[34]:


board.reset


# In[35]:


board.reset_board()


# In[36]:


board


# In[37]:


fen_line = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
board.reset_board()
chessposition,b = fenboard(fen_line)
chessposition


# In[38]:


mov = move_pieces(3)
board.push(mov)
board


# In[ ]:





# In[ ]:





# In[ ]:





# In[39]:
rospy.init_node('chess_ai')
imagel = cv2.imread('chess.png')
imagel=cv2.resize(imagel,(800,800))
a = 0
while True:
    print("Have you done?, If yes please type 1")
    n = int(input("Enter a number:"))
    if n == 1:
        imagemove= cv2.imread('chessmove.png')
        imagemove = cv2.resize(imagemove,(800,800))
        cntrs, hierarchy, image_diff= contour(imagel,imagemove)

        midpoint = chessmove_mid(cntrs,imagel)

        boxes, points =chessboard(imagel)

        yleft, yright, xleft, xright, y1left, y1right, x1left, x1right= midrange(midpoint,points)

        val,x,y,x1,y1 =which_box(boxes,yleft, yright, xleft, xright, y1left, y1right, x1left, x1right)

        key1, key2 = get_key(val)
	
        a,b = movement(chessposition,key1,key2,x,y,x1,y1)
        move = output(a,b)
        print(chessposition)
        
        print(board)
        board.push_san(move)
        print(board)
        mov = move_pieces(3)
        board.push(mov)
        
        string = mov
        tstring = str(string)

        keyop1 = tstring[0]+ tstring[1]
        keyop2 = tstring[2]+ tstring[3]
        print(keyop1)
        key1 = get_val(keyop1)
        key2 = get_val(keyop2)
        print(key1)

        x = key1[0]
        y = key1[1]
        x1 = key2[0]
        y1 = key2[1]
        print(keyop1)
        init, final = movementop(chessposition,keyop1,keyop2,x,y,x1,y1)
        print(final)
        talker(final)
        chessposition
        imagel = cv2.imread('chess.png')
        imagel = cv2.resize(imagel,(800,800))      
        print("Your turn")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




