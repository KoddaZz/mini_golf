# Importation des modules nécessaires au fonctionnement du programme 

import pygame
import sys
import time
from pygame.locals import *
from random import randint
import sqlite3
import pygame_menu
from pygame_menu.widgets.core.widget import Widget
import pygame_menu.widgets
import pygame_menu._widgetmanager
import pygame_menu.events as events
from pygame_menu.events import BACK, CLOSE


DIMENSION = 500
RAYON = 10
trou = 15
touche_paroi = 0
nbr_coups = 1

pygame.display.init()
fenetre = pygame.display.set_mode((DIMENSION, DIMENSION))
fenetre.fill([0, 0, 0])

conn = sqlite3.connect('data.db')
cursor = conn.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     pseudo TEXT,
     password TEXT,
     score INT

)
""")
conn.commit()


pygame.init()

# Initialisation de la surface d'affichage
display_surface = pygame.display.set_mode((DIMENSION, DIMENSION))


def insert_data_score(pseudo, score):
    # Vérifie si l'utilisateur existe dans la base de données
    cursor.execute("SELECT id,score FROM users WHERE pseudo = :pseudo", {"pseudo": pseudo})
    result = cursor.fetchone()

    # L'utilisateur n'existe pas (impossible a ce stade)
    if result is None:
        raise Exception("The given user does not exist: " + pseudo)
    
    # L'utilisateur existe mais son score n'est pas definit ou est superieur
    if result[1] is None or result[1] > score:
        cursor.execute("UPDATE users SET score = :score WHERE id = :user_id", {"score": score, "user_id": result[0]})
        conn.commit()



def pseudo_existant(pseudo):
    test_pseudo = "SELECT * FROM users WHERE pseudo = :pseudo"
    cursor.execute(test_pseudo, {"pseudo": pseudo})

    # Recuperation du resultat
    resultat = cursor.fetchall()

    if len(resultat) == 0:
        return False
    else:
        return True
    

class Balle:     # ici on créé la classe balle
    def __init__(self):
        self.x = randint(RAYON, DIMENSION-RAYON)
        self.y = randint(RAYON, DIMENSION-RAYON)
        self.dx = 0
        self.dy = 0
        self.couleur = (255, 255, 255)
        self.taille = RAYON
        self.hitbox_balle = pygame.Rect(self.x, self.y, self.taille, self.taille)
        self.coeff_frottement = 0.999

    def bouge(self):  # Cette fonction gère les rebondissement de la balle
        pygame.draw.circle(fenetre, (51, 153, 0), (self.x, self.y), self.taille)
        self.x += self.dx * self.coeff_frottement
        self.y += self.dy * self.coeff_frottement

        if self.y < self.taille or self.y > DIMENSION - self.taille:
            self.dy = -self.dy
        if self.x < self.taille or self.x > DIMENSION - self.taille:
            self.dx = -self.dx
        pygame.draw.circle(fenetre, self.couleur, (self.x, self.y), self.taille)

class LePuits:
    def __init__(self):
        self.x2 = 0
        self.y2 = 0
        self.color = (0, 0, 0)
        self.trou = trou
        self.hitbox_trou = pygame.Rect(self.x2, self.y2, self.trou, self.trou)

    def draw(self):
        pygame.draw.circle(fenetre, self.color, (self.x2, self.y2), self.trou)


class Obstacles:
    def __init__(self, x, y, size):
        self.position_x = x
        self.position_y = y
        self.size = size
        self.color = (255, 0, 0)
        self.hitbox_obstacle = pygame.Rect(self.position_x, self.position_y, self.size, self.size)
    def draw(self):

        pygame.draw.rect(fenetre, self.color, (self.position_x, self.position_y, self.size, self.size))

def obtenir_direction_vers_point(point_x, point_y):
    # Calcule la direction (dx, dy) vers le point (point_x, point_y)
    dx = (point_x - ma_balle.x)
    dy = (point_y - ma_balle.y)
    norme = (dx**2 + dy**2)**0.5
    if norme > 0:
        dx /= norme
        dy /= norme
    return dx*norme*0.01, dy*norme*0.01

ma_balle = Balle()
drapeau = LePuits()




def close_menu():
    pygame.quit()

menu = pygame_menu.Menu(
    height=DIMENSION,
    width=DIMENSION,
    title="Mini Golf",
    theme=pygame_menu.themes.THEME_DEFAULT,
)

# Create the "Connexion" menu
menu_connexion = pygame_menu.Menu(
    height=DIMENSION,
    width=DIMENSION,
    title="Connexion",
    theme=pygame_menu.themes.THEME_DEFAULT,
    onclose=CLOSE,
)

# Create the "Inscription" menu
menu_inscription = pygame_menu.Menu(
    height=DIMENSION,
    width=DIMENSION,
    title="Inscription",
    theme=pygame_menu.themes.THEME_DEFAULT,
    onclose=CLOSE,
)

menu_parcours = pygame_menu.Menu(
    height=DIMENSION,
    width=DIMENSION,
    title='Parcours',
    theme=pygame_menu.themes.THEME_DEFAULT,
    onclose=CLOSE,
)

menu_de_fin = pygame_menu.Menu(
    height=DIMENSION,
    width=DIMENSION,
    title='Menu de Fin',
    theme=pygame_menu.themes.THEME_DEFAULT,
    onclose=CLOSE,
)

username_value = ""
password_value = ""

new_user = False


def pseudo_existant(pseudo):
    test_pseudo = "SELECT * FROM users WHERE pseudo = :pseudo"
    cursor.execute(test_pseudo, {"pseudo": pseudo})

    # Recuperation du resultat
    resultat = cursor.fetchall()

    if len(resultat) == 0:
        return False
    else:
        return True
    

def insert_data(data):
    # Exécute la requête SQL
    cursor.execute("INSERT INTO users (pseudo, password) VALUES (:pseudo, :password);", data)
    # Valide les modifications
    conn.commit()




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
    insert_data(data)
    print('Inscription réussie ! :)')
    new_user = True
    menu_inscription.close()
    menu_parcours.mainloop(display_surface)


def parcours():
    global choix_parcours
    if choix_parcours.get_value() not in ['1','2','3']:
        choix_parcours.clear()
        menu_parcours.add.button("Inexistant !")
        menu_parcours.mainloop(display_surface)
    else:
        if choix_parcours.get_value() == '1':
            drapeau.x2 = DIMENSION / 2
            drapeau.y2 = DIMENSION / 10
            menu_parcours.close()
        elif choix_parcours.get_value() =='2':
            drapeau.x2 = DIMENSION / 2
            drapeau.y2 = DIMENSION / 2
            menu_parcours.close()
        else:
            drapeau.x2 = DIMENSION * 0.90
            drapeau.y2 = DIMENSION * 0.10
            menu_parcours.close()
    







menu.add.button("Inscription",accept_kwargs=True, action=menu_inscription)
menu.add.button("Connexion",accept_kwargs=True, action=menu_connexion)
# Menu "Connexion"




username_value = menu_connexion.add.text_input("Username:", default="")
password_value = menu_connexion.add.text_input("Password:", password=True)
menu_connexion.add.button("Connexion", accept_kwargs=True, action=connexion)
menu_connexion.add.button("Quitter", accept_kwargs=True, action=CLOSE)

# Menu "Inscription"
inscription_username_value = menu_inscription.add.text_input("Username:", default="")
inscription_password_value = menu_inscription.add.text_input("Password:", password=True)
menu_inscription.add.button("Inscription", accept_kwargs=True, action=inscription)
menu_inscription.add.button("Quitter", accept_kwargs=True, action=CLOSE)

# Menu Parcours
choix_parcours = menu_parcours.add.text_input("Parcours :",default="")
menu_parcours.add.button("Jouer !", accept_kwargs=True, action=parcours)
menu.mainloop(display_surface)


#Menu de Fin




# Idée à compléter car il faut différents parcours avec différents obstacles ( #TO DO MAJ )
fenetre.fill([51 ,153 , 0])
obstacle1 = Obstacles(200, 200, 20)
obstacle2 = Obstacles(300, 300, 30)

obstacles = [obstacle1,obstacle2]

for obstacle in obstacles:
        obstacle.draw()
#
# CONNEXION / INSCRIPTION JOUEUR
    

while True:
    drapeau.draw()

    for obstacle in obstacles:
        obstacle.draw()
        if ma_balle.hitbox_balle.colliderect(obstacle.hitbox_obstacle):
            ma_balle.dx = -ma_balle.dx
            ma_balle.dy = -ma_balle.dy

        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1: # Représente le CLIC-GAUCHE
            point_x, point_y = pygame.mouse.get_pos()
            ma_balle.dx, ma_balle.dy = obtenir_direction_vers_point(point_x, point_y)
            nbr_coups += 1

    if ma_balle.y < ma_balle.taille or ma_balle.y > DIMENSION - ma_balle.taille:
            touche_paroi +=1
    if ma_balle.x < ma_balle.taille or ma_balle.x > DIMENSION - ma_balle.taille:
            touche_paroi +=1

    speed_magnitude = (ma_balle.dx**2 + ma_balle.dy**2)**0.5  #calcule la magnitude de la vitesse
    if speed_magnitude < 0.1:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                point_x, point_y = pygame.mouse.get_pos()
                ma_balle.dx, ma_balle.dy = obtenir_direction_vers_point(point_x, point_y)
                nbr_coups += 1

    if ma_balle.hitbox_balle.colliderect(drapeau.hitbox_trou) and ma_balle.dx**2 < 2.5 and ma_balle.dy**2 < 2.5 :
        menu_de_fin.add.button( f"Score : {nbr_coups-1}",accept_kwargs=True)
        menu_de_fin.add.button( f"Paroi touchée : {touche_paroi}",accept_kwargs=True)
        menu_de_fin.add.button( "Rejouez ?",accept_kwargs=True)

        if new_user:
            print("Bravo", inscription_username_value.get_value(),"! Vous avez réussi en touchant la paroi  " + str(touche_paroi) + " fois ! Et en " + str(nbr_coups-1) + " coups ! BEAU SWING !")
        #best_score.append(nbr_coups)
            insert_data_score(inscription_username_value.get_value(),(nbr_coups-1))
            menu_de_fin.mainloop(display_surface)
            menu_de_fin.close()
        else:
            print("Bravo", username_value.get_value(),"! Vous avez réussi en touchant la paroi  " + str(touche_paroi) + " fois ! Et en " + str(nbr_coups-1) + " coups ! BEAU SWING !")
            insert_data_score(username_value.get_value(),(nbr_coups-1))
            menu_de_fin.mainloop(display_surface)
            menu_de_fin.close()
        pygame.display.update()
        pygame.display.quit()
        sys.exit()


    ma_balle.bouge()
    ma_balle.hitbox_balle = pygame.Rect(ma_balle.x, ma_balle.y, ma_balle.taille, ma_balle.taille)
    drapeau.hitbox_trou = pygame.Rect(drapeau.x2, drapeau.y2, drapeau.trou,drapeau.trou)
    ma_balle.dx = ma_balle.dx*0.99
    ma_balle.dy = ma_balle.dy*0.99
    pygame.display.update()


    time.sleep(0.03)


# AJOUTE UNE LISTE POUR CONSERVER LE NOMBRE DE COUPS QUE LE JOUEUR A FAIT LA DERNIERE PARTIE, ET QUE CA LUI DISE SON BEST SCORE ET COMPARE LE AVEC LE NOUVEAU RESULTAT POUR VOIR SI C'EST SON NOUVEAU MEILLEUR SCORE
#TO DO MAJ

best_score = []  # création d'une liste pour conserver les meilleurs score du joueurs

best_score.append(nbr_coups)    