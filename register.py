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
DIMENSION = 500
display_surface = pygame.display.set_mode((DIMENSION, DIMENSION))


#Menu Inscription
menu_inscription = pygame_menu.Menu(
    height=DIMENSION,
    width=DIMENSION,
    title="Inscription",
    theme=pygame_menu.themes.THEME_DEFAULT,
    onclose=CLOSE,
)

#Menu Parcours
menu_parcours = pygame_menu.Menu(
    height=DIMENSION,
    width=DIMENSION,
    title='Parcours',
    theme=pygame_menu.themes.THEME_DEFAULT,
    onclose=CLOSE,
)

#Fonction servant à verifier si le pseudo n'est pas déjà utilisé 
def pseudo_existant(pseudo):
    test_pseudo = "SELECT * FROM users WHERE pseudo = :pseudo"
    cursor.execute(test_pseudo, {"pseudo": pseudo})

    # Recuperation du resultat
    resultat = cursor.fetchall()

    if len(resultat) == 0:
        return False
    else:
        return True
    
def inscription():
    global username_value
    global password_value
    global new_user

    username_value = inscription_username_value.get_value()
    password_value = inscription_password_value.get_value()
    data = {}

    # Vérifie si le pseudo existe déjà
    existe = pseudo_existant(username_value)
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
    menu_parcours.mainloop(display_surface)

#Gestion Menu Inscritpion
inscription_username_value = menu_inscription.add.text_input("Username:", default="")
inscription_password_value = menu_inscription.add.text_input("Password:", password=True)
menu_inscription.add.button("Inscription", accept_kwargs=True, action=inscription)
menu_inscription.add.button("Quitter", accept_kwargs=True, action=CLOSE)