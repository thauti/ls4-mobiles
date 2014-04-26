from Noeud import *

class Arbre():

	"""Represente un arbre"""

	def __init__(self, n=None):
		self.noeud = n

	def toText(self):
		if self.noeud==None :
			return '[]'
		else:
			return str(self.noeud.toText())

	def construire_fichier_arbre(self, liste):
		"""Construit l'arbre depuis une liste de noeud et de poids"""

		print(liste)
		self.noeud = Noeud()
		self.noeud.construire_fichier_arbre(liste)

	def getPoids(self):
		""" Retourne le poids total de l'arbre """
		return self.noeud.getPoids()

	def afficher(self,canvas):
		""" Affiche l'arbre"""
		self.noeud.afficher(canvas,700,50,600)

	def getObjPoids(self):
		""" Permet de recuperer la liste des poids (en tant qu'objet)"""
		if self.noeud == None:
			return '[]'
		else:
			liste = []
			self.noeud.getObjPoids(liste)
			return liste