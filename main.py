#coding=UTF-8
import tkinter

from client import *

print("CLIENT v0.1 par Nohan 18/11/2017")

class Application(tkinter.Tk):
	def __init__(self):
		tkinter.Tk.__init__(self)
		self.EnRoute = True
		self.title("Ping.EXE")
		self.geometry("600x600")
		self.resizable(width=False,height=False)
		self.option_add("*Font", "Fixedsys 17")
		#variables
		self.pseudo = tkinter.StringVar()
		self.pseudo.set("Nohan")
		self.cible = tkinter.StringVar()
		self.cible.set("localhost")
		self.port = tkinter.StringVar()
		self.info = tkinter.StringVar()
		
		self.MonscoreStr = tkinter.StringVar()
		self.ScoreOpposantStr = tkinter.StringVar()
		self.Monscore = 0
		self.ScoreOpposant = 0
		
		self.port.set("60600")
		#constructions
		self.Menu_Principal()
		#evenements
		self.mainloop()
	
	def Bind_Touches(self):
		self.bind('<Up>', self.Monter)
		self.bind('<Down>', self.Descendre)
	
	def Menu_Principal(self):
		tkinter.Label(self,text="ping.EXE").grid(
												column=0,
												row=0
												)
		tkinter.Label(self, text="Pseudo:").grid(
												column=0,
												row=1,
												sticky=tkinter.W
												)
		tkinter.Entry(self,width=15,text=self.pseudo,fg="red").grid(
																	column=0,
																	row=2,
																	sticky=tkinter.W
																	)
		tkinter.Label(self, text="On fais quoi ?").grid(
														column=0,
														row=3,
														sticky=tkinter.W
														)
		tkinter.Button(self,text="Créer la salle",command=self.Lancer).grid(column=0,row=4)
		tkinter.Button(self,text="Rejoindre une salle",command=self.Menu_Connexion).grid(column=1,row=4)
		tkinter.Label(self, textvariable=self.info).grid(padx=0,row=5)
		
	
	def Menu_Connexion(self):
		if(len(self.pseudo.get()) == 0):
			self.info.set("Euuh t'est qui ?")
			return
		elif(len(self.pseudo.get()) < 4):
			self.info.set("Euuh c'est quoi ce pseudo ?")
			return
		else:
			self.ClearMenu()
		tkinter.Label(self, text="Ok, maintenant faut que tu me \ndises où est ton pote").grid(column=0,row=1,sticky=tkinter.W,columnspan=2)
		tkinter.Label(self, text="Adresse").grid(column=0,row=3,sticky=tkinter.W)
		tkinter.Label(self, text="Port",anchor=tkinter.W,justify=tkinter.LEFT).grid(column=1,row=3,sticky=tkinter.W)
		tkinter.Entry(self,width=15,text=self.cible,fg="red").grid(column=0,row=4,sticky=tkinter.W)
		tkinter.Entry(self,width=5,text=self.port,fg="red").grid(column=1,row=4,sticky=tkinter.W)
		tkinter.Button(self,text="C'est parti !",command=self.Lancer).grid(column=1,row=5,sticky=tkinter.W)
		tkinter.Label(self, textvariable=self.info,fg='orange').grid(padx=0,row=6,columnspan=4,sticky=tkinter.W)
		
	
	def ClearMenu(self):
		self.info.set("")
		for widget in self.winfo_children():
			widget.destroy()
	
	def Lancer(self):
		if(len(self.cible.get()) == 0):
			self.info.set("T'as pas l'impression d'avoir oublié\n un truc ?")
			return
		self.withdraw()
		self.client = Client(self,self.pseudo.get(),(self.cible.get(),int(self.port.get())))
	
	
	def pret(self):
		self.ClearMenu()
		self.deiconify()
		tkinter.Label(self, text="Vous êtes connecté !\n En attente du serveur").grid(column=0,row=0,sticky=tkinter.W,columnspan=2)
	
	def Serveur_pret(self,opposant):
		self.ClearMenu()
		self.opposant = opposant
		tkinter.Label(self, text="{} VS {} ".format(self.pseudo.get(),self.opposant)).grid(column=1,row=1)
		tkinter.Button(self,text="Prêt",command=self.pret_a_jouer).grid(column=2,row=2)
	
	def pret_a_jouer(self):
		self.client.send("STATUS:PRET".encode())
	
	def lancerPartie(self):
		self.FPS = 120
		
		self.boule = Boule((10,10))
		self.baton1 = Batonnet(1)
		self.baton2 = Batonnet(2)
		
		self.ClearMenu()
		tkinter.Label(self, text="{} VS {}".format(self.pseudo.get(),self.opposant)).grid(column=0,row=0)

		
		self.Feuille = tkinter.Canvas(self, width=600, height=500, bg='#000075')
		self.Feuille.grid(column=0,row=1)
		
		self.MonscoreStr.set("0")
		self.ScoreOpposantStr.set("0")
		
		tkinter.Label(self, textvariable=self.MonscoreStr).grid(column=0,row=2,sticky=tkinter.W)
		tkinter.Label(self, textvariable=self.ScoreOpposantStr).grid(column=0,row=2,sticky=tkinter.E)
		
		
		self.Dessin_Boule = self.Feuille.create_oval(self.boule.getPosX(), self.boule.getPosY(), self.boule.getPosX()+10, self.boule.getPosY()+10, outline='grey',fill='white')
		self.Dessin_baton1 = self.Feuille.create_rectangle(self.baton1.getPosX(),self.baton1.getPosY(),self.baton1.getPosX()+10,self.baton1.getPosY()+100,fill='#8D00FF')
		self.Dessin_baton2 = self.Feuille.create_rectangle(self.baton2.getPosX(),self.baton2.getPosY(),self.baton2.getPosX()+10,self.baton2.getPosY()+100,fill='#8D00FF')
		
		self.Bind_Touches()
		while self.EnRoute:
			time.sleep(1/self.FPS)
			self.Feuille.coords(self.Dessin_Boule,self.boule.getPosX(), self.boule.getPosY(), self.boule.getPosX()+10, self.boule.getPosY()+10)
			self.Feuille.coords(self.Dessin_baton1,self.baton1.getPosX(),self.baton1.getPosY(),self.baton1.getPosX()+10,self.baton1.getPosY()+100)
			self.Feuille.coords(self.Dessin_baton2,self.baton2.getPosX(),self.baton2.getPosY(),self.baton2.getPosX()+10,self.baton2.getPosY()+100)
			self.Feuille.update()
	
	def finPartie(self,jaigagne):
		self.ClearMenu()
		if(jaigagne):
			tkinter.Label(self, text="OMG t'est trop fort t'a gagné").grid(column=0,row=1)
		else:
			tkinter.Label(self, text="S'il te plaît désinstalle moi\nt'as pas le niveau").grid(column=0,row=2)
			tkinter.Button(self,text="Effacer le jeu",command=None).grid(column=0,row=3)
	
	def Descendre(self,event):
		self.client.send("CMD:BAS".encode())
	def Monter(self,event):
		self.client.send("CMD:HAUT".encode())
		
	def ActualiserScores(self,monscore,oppscore):
		self.MonscoreStr.set(monscore)
		self.ScoreOpposantStr.set(oppscore)

			

Application()
