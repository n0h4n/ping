class Position():
	def getPosX(self):
		return int(self.x)
	
	def getPosY(self):
		return int(self.y)
	
	def getPos(self):
		return int(self.x),int(self.y)
	
	def setPosX(self,x):
		self.x = x
	
	def setPosY(self,y):
		self.y = y

class Boule(Position):
	def __init__(self,pos):
		self.x , self.y = pos

class Batonnet(Position):
	def __init__(self,ID):
		if(ID == 1):
			self.x = 10
		if(ID == 2):
			self.x = 580
		self.y = 10
