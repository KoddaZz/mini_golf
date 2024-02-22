##################################################################################################################################################
#
#                         UTILITAIRES POUR LA CONNEXION - JEU MINI GOLF  |  REALISE PAR KoddaZz
#                                                               ©KoddaZz
##################################################################################################################################################

import pygame
import pygame_menu
from pygame_menu.events import CLOSE
import sqlite3

from utilities_db import pseudo_existant

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

username_value =""
password_value =""

DIMENSION = 500

display_surface = pygame.display.set_mode((DIMENSION, DIMENSION))

# Création du menu "Connexion"
menu_connexion = pygame_menu.Menu(
    height=DIMENSION,
    width=DIMENSION,
    title="Connexion",
    theme=pygame_menu.themes.THEME_DEFAULT,
    onclose=CLOSE,
)

# Création du menu "Parcours"
menu_parcours = pygame_menu.Menu(
    height=DIMENSION,
    width=DIMENSION,
    title='Parcours',
    theme=pygame_menu.themes.THEME_DEFAULT,
    onclose=CLOSE,
)

def connexion():
    global username_value
    global password_value
    global new_user
    
    existe = pseudo_existant(username_value.get_value())
    if not existe:
        username_value.clear()
        password_value.clear()
        menu_connexion.add.button("Réessayez ! :)",accept_kwargs=True)
        menu_connexion.mainloop(display_surface)
    else:
        test_existance = "SELECT * FROM users WHERE pseudo = :pseudo AND password = :password"
        cursor.execute(test_existance, {"pseudo":username_value.get_value(), "password":password_value.get_value()})

        resultat = cursor.fetchall()
        
        if len(resultat) == 0: # SI le pseudo entré n'existe pas
            print("Mauvais mot de passe")
            password_value.clear()
            menu_connexion.mainloop(display_surface)
        else:
            print("Connexion Réussie ! :)")
            new_user = False
            menu_connexion.close()
            menu_parcours.mainloop(display_surface)


#Gestion du menu "Connexion"
username_value = menu_connexion.add.text_input("Username:", default="")
password_value = menu_connexion.add.text_input("Password:", password=True)
menu_connexion.add.button("Connexion", accept_kwargs=True, action=connexion)
menu_connexion.add.button("Quitter", accept_kwargs=True, action=CLOSE)