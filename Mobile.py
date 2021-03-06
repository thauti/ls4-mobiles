from math import sqrt

class Mobile():

	"""Implemente un poids"""

	def __init__(self, poids=0):
		print(">>",poids)
		self.poids = poids

	def getPoids(self):
		""" Retourne le poids """
		return self.poids
	def toText(self):
		return self.poids
	def afficher(self, canvas, x=0,y=0,longueur=0):
		""" Dessine le poids"""
		self.x = x
		self.y = y
		if self.poids < 20:
			couleur = 'blue'
		elif (self.poids < 100 and self.poids >=20 ):
			couleur = 'green'
		else:
			couleur = 'red'
		canvas.create_line(x,y,x,y+50)
		y=y+50
		canvas.create_oval(x-3*sqrt(self.poids),y-3*sqrt(self.poids),x+3*sqrt(self.poids),y+3*sqrt(self.poids), fill=couleur)
	def afficher_id(self, canvas, id):
		""" Affiche son ID """
		canvas.create_text(self.x,self.y+50,text=id,fill='white')

	def getObjPoids(self,liste):
		""" Retourne l'objet """
		liste.extend([self])