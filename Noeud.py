from Mobile import *
class Noeud():

	"Défini un noeud"

	def __init__(self, n_droit=None, n_gauche=None):
		self.n_droit=n_droit
		self.n_gauche=n_gauche

	def toText(self):
		return [self.n_gauche.toText(), self.n_droit.toText()]

	def construire_fichier_arbre(self, liste):
		print("o")
		print(liste)
			
		if(type(liste[0]) is list):
			if(len(liste[0])>1) :
				self.n_gauche = Noeud()
				self.n_gauche.construire_fichier_arbre(liste[0])
			else :
				self.n_gauche = Mobile(int(liste[0][0]))	
		else:
			self.n_gauche =  Mobile(int(liste[0]))

		if(type(liste[1]) is list):
			if(len(liste[1])>1) :
				self.n_droit = Noeud()
				self.n_droit.construire_fichier_arbre(liste[1])	
			else :
				self.n_droit = Mobile(int(liste[1][0]))

		else:
			self.n_droit =  Mobile(int(liste[1]))

	def getPoids(self):
		""" Retourne le poids totale du noeud """
		return self.n_gauche.getPoids()+self.n_droit.getPoids()

	def afficher(self, canvas, x=0,y=0,longueur=500):			

		l1 = (self.n_gauche.getPoids()*longueur)/(self.n_gauche.getPoids()+self.n_droit.getPoids()) # Calcul de la longueur
		l2 = longueur-l1 # Reste
		print("l1: ",l1," l2: ",l2)
		canvas.create_line(x,y,x,y+50) # ligne horizontal
		canvas.create_line(x-l2,y+50,x+l1,y+50)
		if longueur > 50:
			longueur = longueur //2
		self.n_gauche.afficher(canvas, x-l2,y+50,longueur)
		self.n_droit.afficher(canvas, x+l1,y+50,longueur)