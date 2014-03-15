class Mobile():

	"""Implemente un Mobile"""

	def __init__(self, poids=0):
		print(">>",poids)
		self.poids = poids

	def getPoids(self):
		return self.poids
	def toText(self):
		return self.poids
	def afficher(self, canvas, x=0,y=0):
		canvas.create_line(x,y,x,y+50)
		y=y+50
		canvas.create_oval(x-15-self.poids,y-15-self.poids,x+15+self.poids,y+15+self.poids, fill="blue")