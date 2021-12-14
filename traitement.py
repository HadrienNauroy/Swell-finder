""" Des fonctions pour le traitement des données issues de tableau_3D """


from time import *


#selection et sub_selection permettent de choisir un instant dans le tableau 3D
def selection(tableau_3D,indice,nb_data):
	res = []
	for k in range(len(tableau_3D)):
		res += [sub_selection(tableau_3D[k],indice,nb_data)]
	return res

def sub_selection(tableau_2D,indice,nb_data):
	res=[]
	for k in range(nb_data) : 
		res += [tableau_2D[k][indice]]
	return res

def projection(tableau_2D, spot_names, spot_orientation):
	i=0
	for spot in spot_names : 
		orientation = spot_orientation.get(spot)
		tableau_2D[i][2]=(tableau_2D[i][2]-orientation)%360 #orientation du vent 
		tableau_2D[i][5]=(tableau_2D[i][5]-orientation)%360 #orientation des vagues
		i+=1
	return tableau_2D

def find_marée(liste):
	#On trouve le temps restant avant la prochaine marée haute
	#NB : on ne considère pas les variations d'un jour à l'autre de la marée 
	#Ce n'est pas si grave si on utilise le programe pour avoir des données sur le jour même
	#pour rappel : liste_marées = matin_heure,matin_minutes,matin_coef,soir_heure,soir_minutes,soir_coef

	heure,minutes = localtime().tm_hour, localtime().tm_min

	#Si la prochaine marée haute est celle du matin
	if heure < liste[0]:
		delta_h = liste[0]-heure
		delta_m = liste[1]-minutes
		coef = liste[2]
		#pour remetre au format dans X heure et Y minutes
		if delta_m < 0 : 
			delta_h -=1
			delta_m +=60

	elif heure == liste[0] and minutes < liste[1] : 
		delta_h = 0
		delta_m = liste[1]-minutes

	#si la prochaine marée haute est celle du soir
	else :
		delta_h = liste[3]-heure
		delta_m = liste[4]-minutes
		coef = liste[2]
		#pour remetre au format dans X heure et Y minutes
		if delta_m < 0 : 
			delta_h -=1
			delta_m +=60

	#si la prochaine marée est le lendemain 
	if delta_h <0 :
		delta_h = liste[0]+25-heure #on considère que l'heure du lendemain est decalée d'une heure
		delta_m = liste[1]-minutes
		#pour remetre au format dans X heure et Y minutes
		if delta_m < 0 : 
			delta_h -=1
			delta_m +=60

	#NB :  On introduit une erreur si l'heure choisie est après l'heure de la marée mais ce n'est pas une erreur enorme
	#corriger ce problème à l'air compliqué on laisse comme ça pour la V1
	#ce sera un plus gros problème quand on voudra faire des prévisions pour le lendemain ou 12h plus tard ...

	return([delta_h,delta_m,coef])
