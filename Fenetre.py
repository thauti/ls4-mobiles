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

		self.canvas = Canvas(self, width=1000, height=1000, bg="white")
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
		texte = [line.rstrip() for line in texte]
		texte[0] = premier_chara+texte[0] # On remet le premier charactère au début

		if premier_chara == '[' : # Si il est du type Arbre
			self.convertir_en_arbre(texte)
		elif int(premier_chara) in range(0,10): # Si c'est un ensemble de poids
			arbre_1 = self.mode_1(texte)
			self.arbre = Arbre()
			self.arbre.construire_fichier_arbre(arbre_1)
			self.ecrire_arbre(arbre_1)
			
			
		else:							# Sinon erreur
			print("Erreur: Ce fichier n'est pas valide")
		fichier.close()

	def convertir_en_arbre(self, texte):
		"""Converti le fichier de type Arbre en objet arbre"""
		print(texte)
		self.arbre = Arbre()
		self.arbre.construire_fichier_arbre(eval(texte[0]))

	def afficher_arbre(self):
		self.canvas.delete('all')
		self.canvas.update()
		self.arbre.afficher(self.canvas)

	def mode_1(self,liste) :
		if len(liste) <= 2 :
			return liste
		milieu = len(liste)//2
		if milieu < 2 :
			return  [liste[0],self.mode_1(liste[milieu:])]
		else :
			return [self.mode_1(liste[:milieu]),self.mode_1(liste[milieu:])]

	#def mode_2(self,liste) :
	
	def ecrire_arbre(self,arbre) :
		
		fichier = open("ArbrePoids.txt","w")
		res="["
		res = res+self.traitement_ecriture(arbre)		
		res= res +"]"
		fichier.write(res)
		fichier.close()


	def traitement_ecriture(self,arbre) :
		res=""
		if type(arbre[0]) is not list :

			res=res+arbre[0]+","
			
		if type(arbre[1]) is not list :
			print(arbre[1])
			res=res+arbre[1]
		
		if type(arbre[0]) is list :
			print(arbre[0])
			res=res+"["+self.traitement_ecriture(arbre[0])+"],"
			
		if type(arbre[1]) is list :			
			res = res +"["+self.traitement_ecriture(arbre[1])+"]"		
		
		return res