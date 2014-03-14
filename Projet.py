from Noeud import *
from Arbre import *
from Mobile import *

monArbre = Arbre()
noeud = Noeud()
noeud2 = Noeud()

mobile1 = Mobile(8)
mobile2 = Mobile(5)
mobile3 = Mobile(3)

noeud2.n_gauche = mobile2
noeud2.n_droit = mobile3
noeud.n_droit = mobile1
noeud.n_gauche = noeud2

monArbre.noeud = noeud

print(monArbre.toText())


""" 
Represente

		X
	/		\
	X		8
  /	 \
 5	  3
 """