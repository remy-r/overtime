#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import os.path
import sys

def toggle():
    name = os.path.dirname(sys.argv[0])+"/.lanceur"
    if t_btn.config('text')[-1] == 'Mettre en pause':
        t_btn.config(text='Au Travail')
        fenetre.configure(background='red')
        champ_label['text'] = "Mode Pause activé"
        if not os.path.isfile(name):
            with open(name, "a") as myfile:
                None
    else:
        t_btn.config(text='Mettre en pause')
        fenetre.configure(background='green')
        champ_label['text'] = "Mode Travail activé"
        if os.path.isfile(name):
            os.remove(name)
    
fenetre = Tk()
fenetre.resizable(width=False, height=False)
fenetre.geometry('{}x{}'.format(300, 100))

name = os.path.dirname(sys.argv[0])+"/.lanceur"

if not os.path.isfile(name):
    champ_label = Label(fenetre, text="Mode Travail activé")
    champ_label.pack()
    t_btn = Button(text="Mettre en pause", width=12, command=toggle)
    t_btn.pack(pady=5)
    fenetre.configure(background='green')
else:
    champ_label = Label(fenetre, text="Mode Pause activé")
    champ_label.pack()
    t_btn = Button(text="Au Travail", width=12, command=toggle)
    t_btn.pack(pady=5)
    fenetre.configure(background='red')
    

fenetre.wm_title("Application de gestion du Temps")
fenetre.mainloop()
