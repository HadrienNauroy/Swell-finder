""" Un script pour noter les conditions """


#C'est un peu le coeur du projet et la partie qui sera sans doute ammenée a être la plus modifiée
#Chaque utilisateur peut apporter ses propres modifications en fonction de ces observation et de sa 
#connaissance des spots pour booster ou affaiblir la note du spot
#NB : les classifications même si elles ont été faites le plus objectivement possible sont sans doute
#biaisées par ma pratique du sport et ne correspondent peut être pas à tous les niveaux !

#les fonctions prennent en entrée un tableau à deux dimensions : 
#	-dimension 1 le spot 
#	-dimension 2 la valeure des données à un instant t 
#
#Les données du tableau sont dans l'ordre : 
#	-vitesse du vent (noeuds)
#	-vitesse des raffales (neouds)
#	-direction relative du vent par rapport au spot (°) (0 = plein mer, 180= plein terre)
#	-la taille de vagues (m)
#	-la periode des vagues (m)
#	-l'orientation des vagues par rapport au spot (°) idem
#
#
#Les fonctions prennent aussi en entrée une liste avec les données de marée :
# 	-heure avant la prochaine marée
#	-minutes avant la prochaine marée
#	-coef de la prochaine marée



#NB : les marées ne sont pas encore prises en compte
#NB : la qualité du spot n'est pas nomplus prise en compte 



def rating_wind(tableau_2D,liste_marée):
	note=[]
	#la note à deux composantes : 
	#	-Une pour le vent (orientation et force)
	#	-Une pour les vagues (taille * période (~puissance))

	#Boucle sur les spots
	for k in range(len(tableau_2D)):

		#Puissance des vagues
		#--------------------
		coef_puissance = tableau_2D[k][3]*tableau_2D[k][4]
		coef_puissance = coef_puissance / 30 #normalisation : le 1 est à 2m 15s
		

		#Orientation de la houle 
		if (tableau_2D[k][5] <45 or tableau_2D[k][5]>315) :
			coef_orientation = 1

		elif (tableau_2D[k][5] <90 or tableau_2D[k][5]>270) : 
			coef_orientation = 0.5

		else : 
			coef_orientation = 0

		#direction du vent 
		#-----------------

		#si vent on shore
		if tableau_2D[k][2]<45 or tableau_2D[k][2]>315 : 
			coef_dir = 1

		#si vent side on
		elif (tableau_2D[k][2] > 45 and tableau_2D[k][2] < 90) or (tableau_2D[k][2] < 315 and tableau_2D[k][2] > 270) : 
			coef_dir = 0.75

		#si vent side off
		elif (tableau_2D[k][2] > 90 and tableau_2D[k][2] < 135) or (tableau_2D[k][2] < 270 and tableau_2D[k][2] > 225) :
			coef_dir = 0.25

		#vent off shore
		else : 
			coef_dir = 0

		#On préfère donc un vent on ou side-on 


		#Force du vent 
		#-------------
		if tableau_2D[k][0] <10 : 
			coef_vit = 0
			coef_puissance = 0 #on peut pas surfer en planche si il n'y a pas de vent

		elif tableau_2D[k][0] <15 : 
			coef_vit = 0.25

		elif tableau_2D[k][0] <20 : 
			coef_vit = 0.5

		elif tableau_2D[k][0] <30 : 
			coef_vit = 1

		elif tableau_2D[k][0] <40 : 
			coef_vit = 0.75

		elif tableau_2D[k][0] <50 : 
			coef_vit = 0.5

		else : 
			coef_vit = 0.25

		#le top c'est donc enre 20 et 30 noeuds

		#si le vent est très raffaleux on diminue un peu la vealeur du coeficient
		if tableau_2D[k][1] - tableau_2D[k][0] >= 10 :
			coef_vit -= 0.25


		note+=[coef_vit*coef_dir + coef_puissance*coef_orientation]
		#20-30 noeuds bien orienté à le même poid que 2m 15s 
		#NB : on pourrait changer et ajouter une pondération

	return(note)

def rating_surf(tableau_2D,liste_marée):
	note=[]

	#Boucle sur les spots
	for k in range(len(tableau_2D)):

		#puissance des vagues
		coef_puissance = tableau_2D[k][3]*tableau_2D[k][4]

		#direction du vent 
		#si vent on shore
		if tableau_2D[k][2]<45 or tableau_2D[k][2]>315 : #vent de mer 
			coef_dir = 0

		#si vent side on
		elif (tableau_2D[k][2] > 45 and tableau_2D[k][2] < 90) or (tableau_2D[k][2] < 315 and tableau_2D[k][2] > 270) : 
			coef_dir = 0.25

		#si vent side off
		elif (tableau_2D[k][2] > 90 and tableau_2D[k][2] < 135) or (tableau_2D[k][2] < 270 and tableau_2D[k][2] > 225) :
			coef_dir = 0.75

		#vent de off shore
		else : 
			coef_dir = 1

		#Orientation de la houle 
		if (tableau_2D[k][5] <45 or tableau_2D[k][5]>315) :
			coef_orientation = 1

		elif (tableau_2D[k][5] <90 or tableau_2D[k][5]>270) : 
			coef_orientation = 0.5

		else : 
			coef_orientation = 0 


		note+=[coef_puissance*coef_orientation*coef_dir]	
		#NB : pas de normalisation nécessaire ici puisqu'on ne compare pas les vagues au vent 

	return(note)