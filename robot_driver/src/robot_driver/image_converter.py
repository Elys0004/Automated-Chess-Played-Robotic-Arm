class image_converter:

  def __init__(self):
    rospy.init_node('image_converter')
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera1/image_raw",ImageMsg,self.callback)
    self.pub = rospy.Publisher('chatter', ImageMsg, queue_size=10)
   

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "rgb8")
    except CvBridgeError as e:
      print(e)
    print(cv_image)
    pub.publish(cv_image)
    crop_image = cv_image[260:540,260:540]
    resize = cv2.resize(crop_image,(800,800))
    cv2.imshow('test', resize)
    print(resize.shape)
    im = Image.fromarray(resize)
    im.save(r'/home/elysia/catkin_ws/src/robot_driver/scripts/chess.png')
    cv2.waitKey(0)
    
