""" Un srcipt python pour trouver des bonnes vagues"""


from tkinter import *
from time import *
from math import *
from Bot import * 
from Bot_marée import * 
from mes_fonctions import *
from traitement import * 
from rating import *
from interface import *


"Initialisation & paramètres"
"---------------------------"

#Un dictionaire avec les ID windguru des spots 
#Region implémentée : Ile de Ré
spot_id={"Pointe du Lizay":"176745","Diamond Head": "1589","Plage des Prises" : "48551" ,"Rivedoux":"48555","Pointe de Grignon" : "48549","La Couarde" : "48552", "Le Gros Jonc" : "48553","Le Martray" : "48550","Les Gouillauds" : "48554"}

#Une liste avec les noms des spots
#spot_names = ["Pointe du Lizay","Diamond Head","Plage des Prises" ,"Rivedoux","Pointe de Grignon" ,"La Couarde" , "Le Gros Jonc","Le Martray","Les Gouillauds"]
spot_names = ["Pointe du Lizay","Diamond Head"] #une liste plus courte pour les tests
#spot_names =["Pointe du Lizay"] #une liste encore plus courte toujours pour les tests

#un dictionaire avec l'orientation des spots
#valeures estimées sur google maps 
#valeures en degré 0=Nord 90=Est 180=Sud etc.
#de la mer vers le spot
spot_orientation = {"Pointe du Lizay":315,"Diamond Head": 0,"Plage des Prises" : 225 ,"Rivedoux": 125 ,"Pointe de Grignon" : 225 ,"La Couarde" : 225, "Le Gros Jonc" : 225,"Le Martray" : 135,"Les Gouillauds" : 230 }

#un dictionnaire avec les heures pour lesquels le spot marche sous forme d'intervales 
#h=0 marée basse, h=6 marée haute (oui on introduit une petite erreur)
#NB : ces données sont aménées à être modifiées
spot_heures = {"Pointe du Lizay":[[3,8]],"Diamond Head": [[3,9]],"Plage des Prises" : [] ,"Rivedoux":[[4,7]],"Pointe de Grignon" :[[0,2],[11,12]],"La Couarde" : [[2,4],[8,10]], "Le Gros Jonc" : [[3,6]],"Le Martray" : [],"Les Gouillauds" : [[0,3],[11,12]]}

tableau_3D=[]
#dimension 1 : le spot
#dimension 2 : la donnée (vitesse vent, taille vagues etc.)
#dimension 3 : le temps (incrément de 3h entre chaque valeure)
n=10 #taille de la plage de donnée

#heure locale
heure=localtime().tm_hour

#Nombre de type de donnée (exept time)
nb_data=6

#pour l'affichage semi-graphique
separateur = "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

"Web Grapping"
"------------"

#marées
print('\n\n\n\n\n\n\n')
print(separateur)
print(separateur)
print('\n\n\nExtraction des données de marées\nVeuillez patienter...\n\n\n')
print(separateur)
print(separateur)
print('\n\n\n\n\n')

bot = Bot_marée()
bot.get_data()
liste_marées = bot.matin_heure,bot.matin_minutes,bot.matin_coef,bot.soir_heure,bot.soir_minutes,bot.soir_coef


#conditions
for spot in spot_names : 

	#affichage terminal pour suivi
	print('\n\n\n\n\n\n\n')
	print(separateur)
	print(separateur)	
	print('\n\n\nExtraction des données de ',spot,'\nVeuillez patienter...\n\n\n')
	print(separateur)
	print(separateur)
	print('\n\n\n\n\n')

	#initialisation des bots
	bot = Bot(ID=spot_id.get(spot),size=n)
	
	#web grapping
	bot.grap()

	#pre traitement (mise en forme des données)
	bot.pre_traitement()
	tableau_3D +=[[bot.liste_vitesse_vent,bot.liste_raffales,bot.liste_direction_vent,bot.liste_taille_vagues, \
	bot.liste_periode_vagues,bot.liste_direction_vagues,bot.time]]

#NB :  le temps est donc redondant dans le tableau mais c'est pour gagner du temps et eviter une connexion web en plus

"Analyse des données"
"-------------------"

#indice de la plus petite heure non passée (pas de 3h sur windguru)
#erreur max 3h c'est acceptable
indice = int((heure - tableau_3D[0][-1])//3 +1)

#dimension 1 : le spot
#dimension 2 : la donnée (vitesse vent, taille vagues etc.)
#On selectione les données correspondants au temps=indice de tableau_3D
tableau_2D = selection(tableau_3D,indice,nb_data)

#On projète l'orientation du vent et des vagues sur celle du spot
#On remplace donc l'angle absolue de ces données par l'angle relatif
#0° = plein mer , 180° = plein terre
tableau_2D = projection(tableau_2D, spot_names, spot_orientation)

#De même on rend relatif l'heure de la prochaine marée haute
marée = find_marée(liste_marées)

#Maintenant que toutes les données sont en place on donne une note à chaque spot
tableau_1D_surf = rating_surf(tableau_2D,marée)
tableau_1D_wind = rating_wind(tableau_2D,marée)

#On recupère la ou les meilleures notes
indices_surf = find_max(tableau_1D_surf)
indices_wind = find_max(tableau_1D_wind)

#On recupère les noms des spots les mieux notés
max_wind = from_ids_to_names(indices_wind,spot_names)
max_surf = from_ids_to_names(indices_surf,spot_names)



#On affiche les resutats
if indices_wind == [] :
	print('\n\n\n\n\n\n\n')
	print(separateur)
	print(separateur)
	print("Il n'y a pas de bon spot pour plancher aujourd'hui")
	print(separateur)
	print(separateur)
	print('\n\n\n\n\n\n\n')

else : 

	print('\n\n\n\n\n\n\n')
	print(separateur)
	print(separateur)	
	print("\n\n\nLe(s) meilleur(s) spot(s) pour plancher aujourd'hui est(sont) : ", max_wind )
	print("\nLe(s) meilleur(s) spot(s) pour surfer aujourd'hui est(sont) : ", max_surf ,'\n\n\n')
	print(separateur)
	print(separateur)
	print('\n\n\n\n\n\n\n')



#I = Interface(spot_names,rating_surf,rating_wind)
'''
i=0
for spot in spot_names : 
	print(spot,' : ', tableau_1D_wind[i])
	i+=1
'''