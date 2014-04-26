from tkinter import *
from tkinter import filedialog
from Arbre import *
import random

class Fenetre(Tk): #Héritage depuis Tk
	def __init__(self):
		
		Tk.__init__(self) #Constructeur de la classe Hérité

		# Titre de la fenêtre principale
		self.title("Construction du mobile")
		self.menubar = Menu(self)
		
		self.frame = Frame(self, bd=0)

		# Menu Fichier
		self.menufichier = Menu(self.menubar, tearoff=0)
		self.menufichier.add_command(label="Ouvrir", command=self.ouvrir_ficher)
		self.menufichier.add_command(label="Enregistrer", command=self.save_fichier)		
		self.menufichier.add_command(label="Quitter", command=self.destroy)
		self.menubar.add_cascade(label="Fichier", menu=self.menufichier)

		# Menu Outils
		self.menuoutil = Menu(self.menubar, tearoff=0)		
		self.menuoutil.add_command(label="Aleatoire", command=self.aleatoire)
		self.menuoutil.add_command(label="Modifier les valeurs", command=self.modif_val)
		self.menubar.add_cascade(label="Outils", menu=self.menuoutil)

		# Menu A propos
		self.menuapropos = Menu(self.menubar, tearoff=0)
		self.menuapropos.add_command(label="A propos", command=self.afficher_apropos)
		self.menubar.add_cascade(label="A propos", menu=self.menuapropos)

		self.v = IntVar()
		self.v.set(1)
		self.menuoption = Menu(self.menubar, tearoff=0)

		# Scroll
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
		"""Fonction d'ouverture de fichier(ouverture seulement) """
		fichier = filedialog.askopenfile(parent=self, title="Ouvrir un mobile")
		# Si on a bien charger un fichier
		if fichier:
			test = self.selection_mode(fichier)
			if test == 1:
				self.afficher_arbre()
			else :
				fichier.close()

	def save_fichier(self):
		""" Fonction de sauvegarde dans un fichier(écriture seulement) """
		print(self.arbre.toText())
		fichier = filedialog.asksaveasfile(parent=self, title="Sauvegarder sous ...")
		if fichier:
			fichier.write(self.arbre.toText())
			fichier.close()

	def modif_val(self):
		""" Création de la fenêtre de gestions des poids"""
		if self.arbre != None:
			self.liste_p = self.arbre.getObjPoids()
		else:
			self.liste_p = []
		
		self.modifval = Toplevel(self)
		self.modifval.minsize(200,200)
		self.modifval.title("Modifier les valeurs")
		bouton_reg = Button(self.modifval,text="Regenerer", command=self.regenerer)
		
		self.liste_input = []

		for i,l in enumerate(self.liste_p):
			print(i, l.poids)
			self.liste_input.append(StringVar())
			self.liste_input[i].set(l.poids)
			Label(self.modifval, text="Poids " +str(i)).grid(column=1,row=i)
			Entry(self.modifval,textvariable=self.liste_input[i]).grid(column=2,row=i)
			l.afficher_id(self.canvas, i)
		bouton_reg.grid(column=1)
		self.modifval.protocol('WM_DELETE_WINDOW', self.modif_val_suppr)
	
	def afficher_apropos(self):
		""" Création de la fenêtre à propos"""
		apropos = Toplevel(self)
		apropos.title("A propos")
		label = Label(apropos, text="Construction de Mobiles \n - LS4 - \n Jérome BETTINELLI - Thomas HAUTIER \n 2013-2014")
		label.pack()
		
	def regenerer(self):
		""" Mise à jour des poids après la modification de leurs valeurs """

		for a,b in enumerate(self.liste_p):
			try:
				if int(self.liste_input[a].get()) < 0:
					self.liste_input[a].set(-int(self.liste_input[a].get()))
				b.poids=int(self.liste_input[a].get())
			except ValueError:
				print("Valeur invalide")
				b.poids = 10
		self.afficher_arbre()
		for a,b in enumerate(self.liste_p):
			b.afficher_id(self.canvas, a)

	def modif_val_suppr(self):
		"""Supression de la fenêtre de changement des valeurs"""
		self.afficher_arbre()
		self.modifval.destroy()

	def safe_cast(self,val, to_type, default=None):
		try :
			return to_type(val)
		except ValueError:
			return default

	def selection_mode(self, fichier):
		"""On regarde quel est le type de fichier"""

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
		""" Boite de dialogue pour choisir l'algo"""
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
		""" Voir ci-dessus """
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
		""" Fonction de mise à jour et d'affichage de l'arbre """
		self.canvas.delete('all')
		self.canvas.update()
		self.arbre.afficher(self.canvas)

	def mode_1(self,liste) :
		""" Algo 1 : """
		if len(liste) <= 2 :
			return liste
		milieu = len(liste)//2
		if milieu < 2 :
			return  [liste[0],self.mode_1(liste[milieu:])]
		else :
			return [self.mode_1(liste[:milieu]),self.mode_1(liste[milieu:])]

	def mode_2(self,liste) :
		""" Algo 2 : """
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
		""" Algo 3 : """
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
		""" Géneration d'un arbre aleatoire"""
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
		""" Algo 4 : """
		liste = [ int(x) for x in liste]		
		

		return self.traitement_mode_4(liste)

	def traitement_mode_4(self,liste) :
		if len(liste)<2 :
			return liste[0]

		l1=[]
		l2=[]

		liste.sort()
		l1.append(liste[len(liste)-1])
		liste=liste[:len(liste)-1]
		l2.append(liste[len(liste)-1])
		liste=liste[:len(liste)-1]

		while(len(liste)>0) :

			if(sum(l1)>sum(l2)) :
				l2.append(liste[0])
			else :
				l1.append(liste[0])
			liste=liste[1:]
		
		return [self.traitement_mode_4(l1),self.traitement_mode_4(l2)]