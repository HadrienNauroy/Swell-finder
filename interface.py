'''un script pour faire une jolie interface pour swell finder'''

from tkinter import *
import os

class Interface() : 


	def __init__(self,spot=[],rating_surf=[],rating_wind=[]) : 

		#initialisation de la fenêtre
		self.master=Tk()
		self.master.title("Swell finder")
		self.master.iconbitmap('vague.ico')
		self.master.geometry("750x500")


		#mettre une image en fond
		bg = PhotoImage(file='fond.png')
		self.canvas=Canvas(self.master, width=750, height=500)
		self.canvas.pack(fill='both',expand=True)
		self.canvas.create_image(0,0,anchor='nw', image=bg)

		#mettre des textes et des bouttons au dessus
		self.canvas.create_text(0,0,anchor='nw', text='Bonjour Alexandre',fill='white')

		self.button = Button(self.master,text='hello')
		self.button_window = self.canvas.create_window(10,10,anchor='nw',window=self.button)


		self.master.mainloop()



if __name__ == "__main__": 
	test = Interface()
