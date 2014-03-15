from tkinter import *
from tkinter import filedialog
from Arbre import *

class Fenetre(Tk): #Héritage depuis Tk
	def __init__(self):
		
		Tk.__init__(self) #Constructeur de la classe Hérité
		self.title("Construction du mobile")

		self.menubar = Menu(self)
		self.menufichier = Menu(self.menubar, tearoff=0)
		self.menufichier.add_command(label="Ouvrir", command=self.ouvrir_ficher)
		self.menufichier.add_command(label="Quitter", command=self.destroy)
		self.menubar.add_cascade(label="Fichier", menu=self.menufichier)

		self.canvas = Canvas(self, width=500, height=500, bg="white")
		self.canvas.pack()
		self.config(menu=self.menubar)

	def ouvrir_ficher(self):

		fichier = filedialog.askopenfile(parent=self, title="Ouvrir un mobile")
		# Si on a bien charger un fichier
		if fichier:
			self.selection_mode(fichier)
			self.afficher_arbre()
		fichier.close()

	def selection_mode(self, fichier):
		"""On regarde quel est le type de fichier"""

		#### AMELIORABLE ####
		premier_chara = fichier.read(1) # On lit le premier charactère de la première ligne
		texte =  fichier.readlines() # On récupère le fichire en liste
		texte[0] = premier_chara+texte[0] # On remet le premier charactère au début

		if premier_chara == '[' : # Si il est du type Arbre
			self.convertir_en_arbre(texte)
		elif int(premier_chara) in range(0,10): # Si c'est un ensemble de poids
			print('Pas encore fait :)')
		else:							# Sinon erreur
			print("Erreur: Ce fichier n'est pas valide")
		fichier.close()

	def convertir_en_arbre(self, texte):
		"""Converti le fichier de type Arbre en objet arbre"""
		print(texte)
		self.arbre = Arbre()
		self.arbre.construire_fichier_arbre(eval(texte[0]))

	def afficher_arbre(self):
		self.arbre.afficher(self.canvas)