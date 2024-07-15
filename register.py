##################################################################################################################################################
#
#                         UTILITAIRES POUR L'INSCRIPTION - JEU MINI GOLF  |  REALISE PAR KoddaZz
#                                                               ©KoddaZz
##################################################################################################################################################

import pygame
import pygame_menu
from pygame_menu.events import CLOSE
import sqlite3

import utilities_db as db


conn = sqlite3.connect('data.db')
cursor = conn.cursor()

username_value =""
password_value =""
new_user = False #-> Valeur par défaut
LONGUEUR = 1000
LARGEUR = 500
display_surface = pygame.display.set_mode((LONGUEUR, LARGEUR))
pygame.init()


#Menu Inscription
menu_inscription = pygame_menu.Menu(
    height=LARGEUR,
    width=LONGUEUR,
    title="Inscription",
    theme=pygame_menu.themes.THEME_DEFAULT,
    onclose=CLOSE,
)


#Fonction qui gère l'inscription du joueur + verifie si pseudo choisi n'existe pas dans la bd
def inscription():
    global username_value
    global password_value
    global new_user

    username_value = inscription_username_value.get_value()
    password_value = inscription_password_value.get_value()
    data = {}

    # Vérifie si le pseudo existe déjà
    existe = db.pseudo_existant(username_value)
    if existe:
        inscription_username_value.clear()
        inscription_password_value.clear()
        menu_inscription.add.button("Pseudo existant !",accept_kwargs=True)
        menu_inscription.mainloop(display_surface)
    data["pseudo"] = inscription_username_value.get_value()
    data["password"] = inscription_password_value.get_value()

        # Insert les données dans la base de données
    db.insert_data(data)
    print('Inscription réussie ! :)')
    new_user = True
    menu_inscription.close()
    



#Gestion Menu Inscritpion
inscription_username_value = menu_inscription.add.text_input("Username:", default="")
inscription_password_value = menu_inscription.add.text_input("Password:", password=True)
menu_inscription.add.button("Inscription", accept_kwargs=True, action=inscription)
menu_inscription.add.button("Quitter", accept_kwargs=True, action=CLOSE)