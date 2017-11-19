
import socket
import threading
from misc import *
import time

class Client(socket.socket,threading.Thread):
	def __init__(self,root,pseudo,cible):
		self.EnRoute = True
		self.info("Lancement du client")
		self.root, self.pseudo, self.cible = root, pseudo, cible
		
		threading.Thread.__init__(self,target=self.EcouterDonnees)
		socket.socket.__init__(self,socket.AF_INET,socket.SOCK_STREAM)
		
		self.info("Connexion au serveur distant: {}".format(cible))
		self.connecter()
		self.info("Le client est prêt")
		

	def info(self,message,type=0):
		if(type == 0):
			self.type_msg = "INFO"
		elif(type == 1):
			self.type_msg = "ATTENTION"
		elif(type == 2):
			self.type_msg = "ERREUR"
		elif(type == 3):
			self.type_msg = "ERREUR FATALE"
		else:
			return
		
		message = "{} [{}] {} ".format(time.strftime("%H:%M:%S"),self.type_msg,message)
		print(message)
		
	def connecter(self):
		for tentative in range(1,6):
			self.info("Connexion à la cible ({}/5)".format(tentative))
			try:
				self.connect(self.cible)
			except Exception as Ex:
				self.info("Echec",2)
				if(tentative == 5):
					self.info("Connexion impossible CODE:{}".format(Ex.__class__.__name__))
					self.root.deiconify()
					self.root.info.set("Impossible de contacter le serveur :(\nVerifie les choses suivantes:\n*Que l'adresse et le port sont corrects\n*Tu est connecté à un réseau\n*Que ton pote a un ordinateur allumé avec\nle jeu dessus")
					return
				else:
					continue
			break
		self.send("Pseudo:{}".format(self.pseudo).encode())
		self.root.pret()
		self.start() #lance le thread
		
	
	def EcouterDonnees(self):
		self.info("Lancement d'un nouveau thread pour l'écoute des donnees")
		while self.EnRoute:
			self.Donnees = self.recv(512).decode()
			#print(self.Donnees)
			self.Donnees = self.Donnees.split(':')
			if(self.Donnees[0] == 'ID'):
				self.ID = self.Donnees[1]
				self.info("Vous êtes de le joueur ({}), {}".format(self.ID,self.pseudo))
			
			if(self.Donnees[0] == 'OPPOSANT'):
				self.opposant = self.Donnees[1]
				self.info("L'autre joueur est {}".format(self.opposant))
			
			if(self.Donnees[0] == 'STATUS'):
				if(self.Donnees[1] == 'PRET'):
					self.info("Le serveur est prêt",1)
					self.root.Serveur_pret(self.opposant)
				if(self.Donnees[1] == 'JEU'):
					threading.Thread(target=self.root.lancerPartie).start()
					self.info("Lancement du la partie !",1)
				if(self.Donnees[1] == 'FIN'):
					self.info("Fin de la partie")
					self.info("En attente des résultats")
				
			if(self.Donnees[0] == 'GAGNANT'):
				self.gagnant = self.Donnees[1]
				self.info("Le gagnant est Joueur {}".format(self.gagnant))
				if(self.gagnant == self.ID):
					self.info("Vous avez gagné !")
					self.root.finPartie(True)
				else:
					self.info("Vous avez perdu :(")
					self.root.finPartie(False)

			if(self.Donnees[0] == 'BOULE'):
				self.root.boule.setPosX(self.Donnees[1])
				self.root.boule.setPosY(self.Donnees[2])
			if(self.Donnees[0] == 'BATONNET'):
				if(self.Donnees[1] == '1'):
					self.root.baton1.setPosY(self.Donnees[2])
				if(self.Donnees[1] == '2'):
					self.root.baton2.setPosY(self.Donnees[2])
			if(self.Donnees[0] == 'SCORE'):
				if(self.Donnees[1] == '1'):
					self.root.Monscore = self.Donnees[2]
				if(self.Donnees[1] == '2'):
					self.root.ScoreOpposant = self.Donnees[2]
				self.root.ActualiserScores(self.root.Monscore,self.root.ScoreOpposant)
				
