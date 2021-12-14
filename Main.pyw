""" Un srcipt python pour trouver des bonnes vagues"""


from tkinter import *
from time import sleep
from math import *
from Bot import * 
from mes_fonctions import *


#Un dictionaire avec les ID windguru des spots 
#Region implémentée : Ile de Ré
spot_id={"Pointe du Lizay":"176745","Diamond Head": "1589","Plage des Prises" : "48551" ,"Rivedoux":"48555","Pointe de Grignon" : "48549","La Couarde" : "48552", "Le Gros Jonc" : "48553","Le Martray" : "48550","Les Gouillauds" : "48554","Bud Bud" : "650316"}
spot_names = ["Pointe du Lizay","Diamond Head","Plage des Prises" ,"Rivedoux","Pointe de Grignon" ,"La Couarde" , "Le Gros Jonc","Le Martray","Les Gouillauds"]

tableau_3D=[]
#dimension 1 : le spot
#dimension 2 : la donnée (vitesse vent, taille vagues etc.)
#dimension 3 : le temps (incrément de 3h entre chaque valeure)
n=10 #la taille des plages de données

for spot in spot_names : 
	#initialisation des bots
	bot = Bot(ID=spot_id.get(spot),n)
	print("\n extraction des données de ",spot)

	#web grapping
	bot.grap()

	#pre traitement (mise en forme des données)
	bot.pre_traitement()
	tableau_3D +=[[bot.liste_vitesse_vent,bot.liste_raffales,bot.liste_direction_vent,bot.liste_taille_vagues, \
	bot.liste_periode_vagues,bot.liste_direction_vagues]]

print(tableau_3D)

master=Tk()

