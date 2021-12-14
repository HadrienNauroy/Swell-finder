"""fichier de fonctions pour faire fonctioner les bots de webgrapping"""

from time import *


def get_data(browser):
	#la fonction get_data prend en entrée un browser sur une page windguru et renvoie toutes les infos utiles
	#on prend le premier modèle sans trop se poser de questions

	#toutes les données sous forme de texte
	elements = browser.find_elements_by_id("tabid_0_0_WINDSPD")
	vitesse_vent = elements[0].text

	elements = browser.find_elements_by_id("tabid_0_0_GUST")
	raffales = elements[0].text

	
	elements = browser.find_elements_by_id("tabid_1_0_HTSGW")
	taille_vagues = elements[0].text

	elements = browser.find_elements_by_id("tabid_1_0_PERPW")
	periode_vagues = elements[0].text

	elements = browser.find_elements_by_id("tabid_1_0_SWELL1")
	taille_houle = elements[0].text

	elements = browser.find_elements_by_id("tabid_1_0_SWPER1")
	periode_houle = elements[0].text

	#heure UTC du début de la plage de donnée
	elements = browser.find_elements_by_id("tabid_0_content_div")
	time = int(elements[0].text[21:23])
	#correction UTC pour prendre en compte la changement d'heure : 
	delta = localtime().tm_hour - gmtime().tm_hour
	time+=delta #heure du début de la plage de donnée en heure locale
	
	#C'est plus dur pour les directions
	n=36 #taille de la plage de donnée
	elements = browser.find_elements_by_class_name("hasSVG")
	direction_vent = [elements[i].get_attribute("title") for i in range(35)]
	direction_vagues = [elements[i].get_attribute("title") for i in range(35,70)]
	direction_houle = [elements[i].get_attribute("title") for i in range(70,105)]

	return(vitesse_vent,raffales,direction_vent,taille_vagues,periode_vagues,direction_vagues,time)



def from_raw_to_liste(raw,n=1,i=0,string='',liste=[]):
	#la fonction prend en entrée un chaine de charactères et une taille et renvoie une liste de taille n
	#contenant les valeurs de la chaine de caratères
	#la fonction est recursive
	chiffres = ['.','0','1','2','3','4','5','6','7','8','9']
	if n == 0 : 
		return(liste)
	if raw[i] in chiffres : 
		return(from_raw_to_liste(raw,n,i+1,string+raw[i],liste))
	else : 
		if string!='':
			return from_raw_to_liste(raw,n-1,i+1,'',liste+[float(string)])

	return from_raw_to_liste(raw,n,i+1,'',liste)


def from_raw_to_liste_2(raw,n=1,i=0,j=0,string='',liste=[]):
	#la fonction prend en entrée une liste de chaines de charactères et une taille et renvoie une liste de taille n
	#contenant les valeurs de la liste de chaine de caratères
	#la fonction est recursive
	chiffres = ['.','0','1','2','3','4','5','6','7','8','9']
	if n == 0 :
		return(liste)
	if raw[i][j] in chiffres : 
		return(from_raw_to_liste_2(raw,n,i,j+1,string+raw[i][j],liste))
	else : 
		if string != '' : 
			return(from_raw_to_liste_2(raw,n-1,i+1,0,'',liste+[int(string)]))

	return(from_raw_to_liste_2(raw,n,i,j+1,'',liste))

def from_raw_to_liste_3(texte):
	#la fonction prend en entrée un texte avec les heures et les coefs de marée haute et renvoie une liste
	matin_heure = int(texte[0:2])
	matin_minutes = int(texte[3:5])
	matin_coef = int(texte[6:8])
	if texte[9:11] =='--':
		soir_heure = matin_heure+12
		soir_minutes = matin_minutes
		soir_coef =matin_coef
	else : 
		soir_heure = int(texte[9:11])
		soir_minutes = int(texte[12:14])
		soir_coef = int(texte[15:17])
	return(matin_heure,matin_minutes,matin_coef,soir_heure,soir_minutes,soir_coef)

	#NB : le soir il peut y avoir '--' si la marée est trop décalée pour soir heure et soir coef
	#On choisi ici de faire une petite erreur sur l'heure de marée en prennant l'heure du matin +12
	#Ca ne change pas grand chose car si c'est la cas la marée est très tard et c'est l'heure du matin qui
	#edst prise en compte



def find_max(liste):
	#La fonction renvoi l'indice du maximum de la liste
	#si il y a égalité elle renvoit tous les indices
	max = 0 
	indice = [] #on renvoi une liste vide si toutes les notes sont égales à 0
	for k in range(len(liste)) : 
		if liste[k] > max:
			max =  liste[k]
			indice = [k]
		elif liste[k] == max:
			max =  liste[k]
			indice += [k]

	return indice

def from_ids_to_names(liste,spot_names) : 
	#la fonction renvoie une chaine de caractère avec tous les noms de spots correspondant aux indices
	res=""
	for i in liste: 
		if res != "":
			res += ", "
		res += spot_names[i]
	return res