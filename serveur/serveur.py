#coding=UTF-8

import socket
import time
import threading
from conf import *

print("SERVEUR v0.1 par Nohan 18/11/2017")

class Serveur(socket.socket):
	def __init__(self,adresse):
		self.EnRoute = True
		self.EnJeu = True
		
		self.info("Lecture de la configuration")
		fichier = Fichier()
		self.max_score = fichier.max_score
		fichier.Decharger()
		
		socket.socket.__init__(self,socket.AF_INET,socket.SOCK_STREAM)
		self.info("Lancement du serveur sur {}".format(adresse))
		self.adresse = adresse
		self.bind(self.adresse)
		self.info("Serveur lancé")
		self.EcouterConnexions()
	
	def EcouterConnexions(self): #On recupere les objets connexion des deux clients
		self.listen(2)
		self.info("En attente de connexion") 
		self.Joueur1, joueur1info = self.accept()
		self.info("Joueur 1 connecté {}".format(joueur1info))
		self.client1 = Client(self,self.Joueur1,joueur1info,1) #Instance de client Joueur 1
		self.Joueur1.send("ID:1".encode())
		
		self.Joueur2, joueur2info = self.accept()
		self.info("Joueur 2 connecté {}".format(joueur2info))  #Instance de client Joueur 2
		self.client2 = Client(self,self.Joueur2,joueur2info,2)
		self.Joueur2.send("ID:2".encode())

		time.sleep(1) #POURQUOI SI ON ATTENDS PAS CE TEMPS LA CA PARS EN COUILLES A LA RECEPTION
		self.Joueur1.send("OPPOSANT:{}".format(self.client2.get_pseudo()).encode()) #On renseigne les clients sur leurs opposant respectif
		self.Joueur2.send("OPPOSANT:{}".format(self.client1.get_pseudo()).encode()) 
		
		self.boule = Boule(self)
		self.batonnet1 = Batonnet(1)
		self.batonnet2 = Batonnet(2)
		
		self.Joueur1.send("STATUS:PRET".encode()) # On renseigne les clients sur le status du serveur
		self.Joueur2.send("STATUS:PRET".encode())
		
		
		
		self.MainLoop()
		
	
	def MainLoop(self):
		self.frequence = 60 #Hz
		self.info("En attente des joueurs ...")
		while not(self.client1.est_pret() & self.client2.est_pret()): #On attends que les joueurs soient pret
			time.sleep(0.1)
		self.info("Lancement de la partie",1)
		self.Joueur1.send("STATUS:JEU".encode()) # On renseigne les clients sur le status du serveur
		self.Joueur2.send("STATUS:JEU".encode())
		while self.EnRoute:
			time.sleep(1/self.frequence/7)
			Client.envoyerTous("BOULE:{}".format(self.boule.getPosStr()))
			time.sleep(1/self.frequence/7)
			Client.envoyerTous("BATONNET:{}:{}".format(self.batonnet1.getIDstr(),self.batonnet1.getPosStr()))
			time.sleep(1/self.frequence/7)
			Client.envoyerTous("BATONNET:{}:{}".format(self.batonnet2.getIDstr(),self.batonnet2.getPosStr()))
			time.sleep(1/self.frequence/7)
			
			if(self.EnJeu):
				self.boule.Avancer()
			
			for client in Client.liste:
				if(client.score >= self.max_score):
					time.sleep(1/self.frequence/7)
					Client.envoyerTous("STATUS:FIN")
					time.sleep(1/self.frequence/7)
					Client.envoyerTous("GAGNANT:{}".format(client.ID))
					time.sleep(1000)
				
	
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




class Client(threading.Thread):
	liste = list()
	def __init__(self,Serveur,connexion,infos,ID):
		self.score = 0
		self.EnRoute = True
		self.Pret = False
		Client.liste.append(self)
		self.Serveur, self.connexion, self.infos = Serveur, connexion, infos
		self.ID = ID
		#connexion.send("ID:{}".format(self.ID).encode())
		self.pseudo = "Inconnue"
		threading.Thread.__init__(self,target=self.ecouterDonnees)
		self.start()
		self.Serveur.info("Lancement d'un nouveau thread pour un nouveau client")

	def envoyerTous(message):
		for client in Client.liste:
			client.connexion.send(message.encode())
	
	def ecouterDonnees(self):
		while self.EnRoute:
			self.Donnees = self.connexion.recv(512).decode()
			self.Donnees = self.Donnees.split(':')
			if(self.Donnees[0] == 'Pseudo'):
				self.pseudo = self.Donnees[1]
				self.Serveur.info("{} est Joueur {}".format(self.pseudo,self.ID))
			if(self.Donnees[0] == 'STATUS'):
				if(self.Donnees[1] == 'PRET'):
					self.Pret = True
			if(self.Donnees[0] == 'CMD'):
				if(self.Donnees[1] == 'HAUT'):
					Batonnet.get(self.ID).up()
				if(self.Donnees[1] == 'BAS'):
					Batonnet.get(self.ID).down()
	def get_pseudo(self):
		return self.pseudo

	def est_pret(self):
		return self.Pret


class Boule():
	def __init__(self,App):
		self.App = App
		self.vitesse = 1
		self.x, self.y = 300, 250
		self.Vx, self.Vy = 3,3
	
	def envoyerPosition(self,connexions):
		for connexion in connexions:
			connexion.send('BOULE:{}:{}'.format(self.x,self.y))
	
	def getPosStr(self):
		return "{}:{}".format(self.x,self.y)

	def Avancer(self):
		if(self.y > 490 or self.y < 0):
			self.Vy = self.Vy * -1
		for batonnet in Batonnet.liste:
			if(self.x+10 > batonnet.x and self.x < batonnet.x+batonnet.taillex):
				if(self.y > batonnet.y and self.y < batonnet.y+batonnet.tailley):
					self.Vx, self.Vy = self.vitesse+int((3+float(str(time.time())[11]))/2), self.vitesse+int((3+float(str(time.time())[12]))/2)
					self.vitesse =+ 1
					if(batonnet.ID == 2):
						self.Vx = self.Vx * -1
		
		if(self.x < 0):
			self.App.client2.score = self.App.client2.score +1 
			self.x = 300
			self.Vx = self.Vx*-1
			self.App.info("Le joueur 2 a {}".format(self.App.client2.score))
			Client.envoyerTous("SCORE:2:{}".format(self.App.client1.score))
			
		if(self.x > 590):
			self.App.client1.score = self.App.client1.score +1
			self.x = 300
			self.Vx = self.Vx*-1
			self.App.info("Le joueur 1 a {}".format(self.App.client1.score))
			Client.envoyerTous("SCORE:1:{}".format(self.App.client1.score))
		
		self.x = self.x + self.Vx
		self.y = self.y + self.Vy

class Batonnet():
	liste = list()
	def __init__(self,ID):
		if(ID == 1):
			self.x = 10
		if(ID == 2):
			self.x = 580
		self.y = 100
		self.tailley = 100
		self.taillex = 10
		self.ID = ID
		self.vitesse = 10
		Batonnet.liste.append(self)
	
	def get(ID):
		for baton in Batonnet.liste:
			if(baton.ID == ID):
				return baton
		
	def envoyerPosition(self,connexions):
		for connexion in connexions:
			connexion.send('BATONNET:{}:{}'.format(self.ID,self.x))
		
	def getPosStr(self):
		return str(self.y)
	
	def getIDstr(self):
		return str(self.ID)
	
	def getID(self):
		return self.ID
	
	def down(self):
		if(self.y < 400):
			self.y = self.y + self.vitesse
	
	def up(self):
		if(self.y > 0):
			self.y = self.y - self.vitesse

hote = input("Entrez l'adresse de l'hote (défault=localhost): ")
port = input("Entrez le port (défault=60600): ")

if(hote == ""):
	hote = "127.0.0.1"
if(port == ""):
	port = 60600
else:
	port = int(port)
	
Serveur((hote,port))
