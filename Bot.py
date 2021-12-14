"""Une classe Bot qui sert à recuperer les données sur internet et les mettre sous forme de liste"""


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from mes_fonctions import *
import os


#suppression des affichages de webdriver-manager
os.environ['WDM_LOG_LEVEL'] = '0'
os.environ['WDM_PRINT_FIRST_LINE'] = 'False'

class Bot() :

	def __init__(self,ID,size=1):
		#ID = ID windguru du spot
		#size = taille de la plage de donnée que l'on veut récuperer, (taille max 35 et 1 par defaut) 

		self.ID = ID

		if size>35 : 
			self.size = 35
		else :
			self.size = size
		#maybe soulever une erreur serait mieux


	def grap(self):
		#Extarire les données sur le web


		# Initialiser le navigateur 
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		#self.browser = webdriver.Chrome('chromedriver', chrome_options=options)

		self.browser  = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options) 
		#en utilisant webdriver manager
		self.browser.set_window_size(1350, 800)


		#Ouvrir windguru
		self.browser.get('https://old.windguru.cz/fr/index.php?sc='+self.ID+'&sty=m_spot/')
		#sleep(5)

		#recuperer les données sous forme de chaine de caractère
		self.vitesse_vent,self.raffales,self.direction_vent,self.taille_vagues,self.periode_vagues,self.direction_vagues, self.time = get_data(self.browser)

		#fermer le navigateur dont on n'a plus besoin
		self.browser.close()
		


	def pre_traitement(self):
		#On transforme les données web peu pratiques en liste de valeures
		self.liste_vitesse_vent=from_raw_to_liste(self.vitesse_vent,self.size)
		self.liste_raffales=from_raw_to_liste(self.raffales,self.size)
		self.liste_taille_vagues=from_raw_to_liste(self.taille_vagues,self.size)
		self.liste_periode_vagues=from_raw_to_liste(self.periode_vagues,self.size)
		self.liste_direction_vent=from_raw_to_liste_2(self.direction_vent,self.size)
		self.liste_direction_vagues=from_raw_to_liste_2(self.direction_vagues,self.size)

	def __repr__(self) : 
		return("Je suis un Bot qui va récupérer les données de vent pour " + str(self.ID) )