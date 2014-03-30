from math import sqrt

class Mobile():

	"""Implemente un Mobile"""

	def __init__(self, poids=0):
		print(">>",poids)
		self.poids = poids

	def getPoids(self):
		return self.poids
	def toText(self):
		return self.poids
	def afficher(self, canvas, x=0,y=0,longueur=0):
		if self.poids < 20:
			couleur = 'blue'
		elif (self.poids < 100 and self.poids >=20 ):
			couleur = 'green'
		else:
			couleur = 'red'
		canvas.create_line(x,y,x,y+50)
		y=y+50
		canvas.create_oval(x-3*sqrt(self.poids),y-3*sqrt(self.poids),x+3*sqrt(self.poids),y+3*sqrt(self.poids), fill=couleur)