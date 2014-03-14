from Noeud import *

class Arbre():

	"""Represente un arbre"""

	def __init__(self, n=None):
		self.noeud = n

	def toText(self):
		return self.noeud.toText()

	def construire_fichier_arbre(self, liste):
		"""Construit l'arbre depuis une liste de noeud et de poids"""

		print(liste)
		self.noeud = Noeud()
		self.noeud.construire_fichier_arbre(liste)

	def getPoids(self):
		return self.noeud.getPoids()

	def afficher(self,canvas):
		self.noeud.afficher(canvas, 250,50)