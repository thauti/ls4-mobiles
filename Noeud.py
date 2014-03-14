class Noeud():
	"Défini un noeud"
	def __init__(self, n_droit=None, n_gauche=None):
		self.n_droit=n_droit
		self.n_gauche=n_gauche
	def toText(self):
		return [self.n_gauche.toText(), self.n_droit.toText()]