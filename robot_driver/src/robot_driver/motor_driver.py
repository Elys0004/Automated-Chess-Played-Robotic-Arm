class MotorDriver:

	def __init__(self, max_speed = 10):
		
		self.max_speed = max_speed
		self.current_speed = 0
		self.voltage = 12
		self.temperature = 47
	
	def set_speed(self, speed):
		
		if speed <= self.max_speed:
			self.current_speed = speed
		else:
			self.current_speed = self.max_speed
	def get_speed(self):
		return self.current_speed
		
