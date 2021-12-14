"""Une classe Bot qui sert à recuperer les données des marées sur internet """

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from mes_fonctions import *
import os


#suppression des affichages de webdriver-manager
os.environ['WDM_LOG_LEVEL'] = '0'
os.environ['WDM_PRINT_FIRST_LINE'] = 'False'

class Bot_marée() :

	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.browser  = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options) 
		#self.browser = webdriver.Chrome('chromedriver', chrome_options=options)
		self.browser.get('https://www.iledere.com/s-informer/s-informer-localement/horaires-de-marees')


	def get_data(self):
		texte = self.browser.find_elements_by_class_name('active')[-1].text 
		self.matin_heure,self.matin_minutes,self.matin_coef,self.soir_heure,self.soir_minutes,\
		self.soir_coef= from_raw_to_liste_3(texte)
		self.browser.close()

	def __repr__(self):
		return "Je suis un bot qui va récupérer les données de marrées ici : 'https://www.iledere.com/s-informer/s-informer-localement/horaires-de-marees'"