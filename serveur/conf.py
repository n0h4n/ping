
class Fichier():
	def __init__(self):
		self.fichier = open('serveur.cfg','r')
		for line in self.fichier.readlines():
			line = line.replace('\n','')
			items = line.split(':')
			self.Traiter(items)
		
	def Traiter(self,items):
		variable = items[0]
		valeur = items[1]
		if(variable == 'max_score'):
			self.max_score = int(valeur)
		elif(variable == 'frequence'):
			self.frequence = valeur
		else:
			pass
	
	def Decharger(self):
		self.fichier.close()
