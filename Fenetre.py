from tkinter import *
from tkinter import filedialog
from Arbre import *
import random

class Fenetre(Tk): #Héritage depuis Tk
	def __init__(self):
		
		Tk.__init__(self) #Constructeur de la classe Hérité
		self.title("Construction du mobile")
		self.menubar = Menu(self)
		
		self.frame = Frame(self, bd=0)

		self.menufichier = Menu(self.menubar, tearoff=0)
		self.menufichier.add_command(label="Ouvrir", command=self.ouvrir_ficher)
		self.menufichier.add_command(label="Enregistrer", command=self.save_fichier)		
		self.menufichier.add_command(label="Quitter", command=self.destroy)
		self.menubar.add_cascade(label="Fichier", menu=self.menufichier)

		self.menuoutil = Menu(self.menubar, tearoff=0)		
		self.menuoutil.add_command(label="Aleatoire", command=self.aleatoire)		
		self.menubar.add_cascade(label="Outil", menu=self.menuoutil)

		self.v = IntVar()
		self.v.set(1)
		self.menuoption = Menu(self.menubar, tearoff=0)
		self.menuoption.add_radiobutton(label='Mode 1', var=self.v, value=1)
		self.menuoption.add_radiobutton(label='Mode 2', var=self.v, value=2)
		self.menuoption.add_radiobutton(label='Mode 3', var=self.v, value=3)				
		self.menubar.add_cascade(label="Option", menu=self.menuoption)	

		self.canvas = Canvas(self.frame, width=800, height=800, bg="white", scrollregion=(0,0,1500,1000))
		self.xscrollbar = Scrollbar(self.frame, orient=HORIZONTAL, command=self.canvas.xview)
		self.yscrollbar = Scrollbar(self.frame, command=self.canvas.yview)
		
		self.canvas.configure(xscrollcommand=self.xscrollbar.set,yscrollcommand=self.yscrollbar.set)

		self.xscrollbar.pack(side="top",fill=BOTH,  expand=0)
		self.yscrollbar.pack(side="right",fill=BOTH,  expand=0)

		self.config(menu=self.menubar)

		self.frame.pack(fill=BOTH, expand=1)
		self.canvas.pack(fill=BOTH, expand=1)
		self.arbre = Arbre() # On crée un arbre nulle

	def ouvrir_ficher(self):

		fichier = filedialog.askopenfile(parent=self, title="Ouvrir un mobile")
		# Si on a bien charger un fichier
		if fichier:
			test = self.selection_mode(fichier)
			if test == 1:
				self.afficher_arbre()
			else :
				fichier.close()

	def save_fichier(self):
		print(self.arbre.toText())
		fichier = filedialog.asksaveasfile(parent=self, title="Sauvegarder sous ...")
		if fichier:
			fichier.write(self.arbre.toText())
			fichier.close()

	def safe_cast(self,val, to_type, default=None):
		try :
			return to_type(val)
		except ValueError:
			return default

	def selection_mode(self, fichier):
		"""On regarde quel est le type de fichier"""

		#### AMELIORABLE ####

		premier_chara = fichier.read(1) # On lit le premier charactère de la première ligne
		texte =  fichier.readlines() # On récupère le fichier en liste
		texte = [line.rstrip() for line in texte]
		texte[0] = premier_chara+texte[0] # On remet le premier charactère au début
		
		try:
			if premier_chara == '[' : # Si il est du type Arbre
				self.convertir_en_arbre(texte)
			elif all(self.safe_cast(x,int) for x in texte) != None :  #Si c'est un ensemble de poids
				self.arbre = Arbre()
				self.construire_modechooser()
				if self.mode == 1 :
					arbre_1 = self.mode_1(texte)
				if self.mode == 2 :
					arbre_1 = self.mode_2(texte)
				if self.mode == 3 :
					arbre_1 = self.mode_3(texte)
				if self.mode == 4 :
					arbre_1 = self.mode_4(texte)	
				
				self.arbre.construire_fichier_arbre(arbre_1)
			fichier.close()
			return 1
		except:							# Sinon erreur
			print("Erreur: Ce fichier n'est pas valide")
			fichier.close()
			return 0

	def construire_modechooser(self):
		self.modechooser = Toplevel(self)
		self.modechooser.title("Choisir le mode")

		liste_label = Label(self.modechooser, text="Veuillez choisir le mode d'ouverture")
		self.liste_mode = Listbox(self.modechooser)

		for i in ['Mode 1', 'Mode 2', 'Mode 3','Mode 4']:
			self.liste_mode.insert(END, i)
		liste_bouton = Button(self.modechooser, text="Valider",command=self.choisir_mode)
		liste_label.pack()
		self.liste_mode.pack()
		liste_bouton.pack()
		self.modechooser.mainloop()

	def choisir_mode(self):
		dic = dict()	
		dic['Mode 1'] = 1
		dic['Mode 2'] = 2
		dic['Mode 3'] = 3
		dic['Mode 4'] = 4
		print("Mode", dic[self.liste_mode.get(ACTIVE)])
		self.mode = dic[self.liste_mode.get(ACTIVE)]
		self.modechooser.quit()
		self.modechooser.destroy()

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

	def mode_2(self,liste) :
		liste = [ int(x) for x in liste]
		liste.sort()
		
		liste_1 =[x for i,x in enumerate(liste) if (i%2==0)]
		liste_2 =[x for i,x in enumerate(liste) if (i%2==1)]
		
		liste_1 = self.traitement_mode_2(liste_1)
		liste_2 = self.traitement_mode_2(liste_2)
	
				
		return [liste_1,liste_2]


	def traitement_mode_2(self,liste) :
		if len(liste) <=2 :
			return liste
		print(liste)
		return[liste[-1],self.traitement_mode_2(liste[:len(liste)-1])]


	def mode_3(self,liste):
		liste = [ int(x) for x in liste]
		liste.sort()
		
		liste_1 =[x for i,x in enumerate(liste) if (i%2==0)]
		liste_2 =[x for i,x in enumerate(liste) if (i%2==1)]
		
		liste_1 = self.traitement_mode_3(liste_1)
		liste_2 = self.traitement_mode_3(liste_2)
	
				
		return [liste_1,liste_2]

	

	def traitement_mode_3(self,liste) :
		if len(liste) <=2 :
			return liste
		print(liste)
		return[self.traitement_mode_3_bis(liste[:len(liste)-1]),liste[-1]]


	def traitement_mode_3_bis(self,liste) :
		if len(liste) <=2 :
			return liste
		print(liste)
		return[liste[-1],self.traitement_mode_3(liste[:len(liste)-1])]


	def aleatoire (self) :
		liste=[random.randrange(1,150) for i in range(random.randrange(2,20))]
		n=random.randrange(1,4)
		if n==1 :
			liste=self.mode_1(liste)
		elif n == 2 :
			liste=self.mode_2(liste)
		elif n == 3 :
			liste=self.mode_3(liste)
		else :
			liste=self.mode_4(liste)
		self.arbre = Arbre()
		self.arbre.construire_fichier_arbre(liste)
		self.afficher_arbre()

	def mode_4(self,liste) :
		liste = [ int(x) for x in liste]		
		

		return self.traitement_mode_4(liste)

	def traitement_mode_4(self,liste) :
		if len(liste)<2 :
			return liste[0]

		l1=[]
		l2=[]

		liste.sort()
		l1.append(max(liste))
		liste=liste[:len(liste)-1]
		l2.append(max(liste))
		liste=liste[:len(liste)-1]

		while(len(liste)>0) :

			if(sum(l1)>sum(l2)) :
				l2.append(max(liste))
			else :
				l1.append(max(liste))
			liste=liste[:len(liste)-1]
		
		return [self.traitement_mode_4(l1),self.traitement_mode_4(l2)]