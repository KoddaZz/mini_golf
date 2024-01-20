
import pygame
import sys
import time
from pygame.locals import *
from random import randint
import sqlite3

# randint(0,10) -> nb aléatoire entre 0 et 10

LARGEUR = 500
HAUTEUR = 500
RAYON = 10
trou = 15
touche_paroi = 0
nbr_coups = 1

pygame.display.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
fenetre.fill([0, 0, 0])

conn = sqlite3.connect('data.db')
cursor = conn.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     pseudo TEXT,
     password TEXT
)
""")
conn.commit()

def insert_data(data):
    # Récupère les valeurs de la requête SQL
    pseudo = data["pseudo"]
    password = data["password"]

    # Exécute la requête SQL
    cursor.execute(
    "INSERT INTO users (pseudo, password) VALUES (:pseudo, :password);",
    {"pseudo": pseudo, "password": password},
)

    # Valide les modifications
    conn.commit()


def acceuil_joueur():
    acceuil = input("Avez vous déjà joué ?")
    assert acceuil in ["Oui","Non","oui","non"], "Répondez par oui ou par non"
    if acceuil in ["oui","Oui"]:
        connexion()
    else:
        inscription()


def connexion():
    pseudo = str(input("Quelle est votre pseudo ?"))
    password = input("Quel est votre mot de passe ?")
    test_existance = "SELECT * FROM users WHERE pseudo = :pseudo AND password = :password"
    cursor.execute(test_existance, {"pseudo":pseudo, "password":password})

    # Recuperation du resultat
    resultat = cursor.fetchall()

    if len(resultat) == 0:
        print("Veuillez réessayer !")
    else:
        print("Connexion Réussie ! :)")

def inscription():
    data = {}
    pseudo = input("Quel est votre pseudo")

    # Vérifie si le pseudo existe déjà
    existe = pseudo_existant(pseudo)
    while existe:
        print("Ce pseudo est déjà utilisé veuillez en réutiliser un autre !")
        pseudo = input("Quel est votre pseudo")
        existe = pseudo_existant(pseudo)
    data["pseudo"] = pseudo
    password = input("Entrez votre mot de passe !")
    data["password"] = password

        # Insert les données dans la base de données
    insert_data(data)
    return True



def pseudo_existant(pseudo):
    test_pseudo = "SELECT * FROM users WHERE pseudo = :pseudo"
    cursor.execute(test_pseudo, {"pseudo": pseudo})

    # Recuperation du resultat
    resultat = cursor.fetchall()

    if len(resultat) == 0:
        return False
    else:
        return True
    








# else si le joueur est inexistant -> INSCRIRE LE JOUEUR ( fonction inscrire ) 

#def connexion(pseudo):
    # reprendre les donneés existantes du joueur
#def inscription_joueur(pseudo):
    # inscrire le joueur ( pseudo / password )


class Balle:     # ici on créé la classe balle
    def __init__(self):
        self.x = randint(RAYON, LARGEUR-RAYON)
        self.y = randint(RAYON, HAUTEUR-RAYON)
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

        if self.y < self.taille or self.y > HAUTEUR - self.taille:
            self.dy = -self.dy
        if self.x < self.taille or self.x > LARGEUR - self.taille:
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
fenetre.fill([51 ,153 , 0])
obstacle1 = Obstacles(200, 200, 20)
obstacle2 = Obstacles(300, 300, 30)

obstacles = [obstacle1,obstacle2]

for obstacle in obstacles:
        obstacle.draw()

# Idée à compléter car il faut différents parcours avec différents obstacles ( #TO DO MAJ )
ask_player_option = int(input("Quelle option choisissez vous ?"))
assert ask_player_option in [1,2,3], "Il n'y a que 3 options pour le moment"
if ask_player_option == 1: # EN HAUT AU MILIEU
    drapeau.x2 = LARGEUR / 2
    drapeau.y2 = HAUTEUR / 10
elif ask_player_option == 2:              # AU MILIEU
    drapeau.x2 = LARGEUR / 2
    drapeau.y2 = HAUTEUR / 2
else:                                     # EN HAUT A GAUCHE
    drapeau.x2 = LARGEUR * 0.90
    drapeau.y2 = HAUTEUR * 0.10

# CONNEXION / INSCRIPTION JOUEUR
    
acceuil_joueur()
while True:
    print(ma_balle.dx, ma_balle.dy)
    drapeau.draw()

    for obstacle in obstacles:

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

    if ma_balle.y < ma_balle.taille or ma_balle.y > HAUTEUR - ma_balle.taille:
            touche_paroi +=1
    if ma_balle.x < ma_balle.taille or ma_balle.x > LARGEUR - ma_balle.taille:
            touche_paroi +=1

    speed_magnitude = (ma_balle.dx**2 + ma_balle.dy**2)**0.5  #calcule la magnitude de la vitesse
    if speed_magnitude < 0.1:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                point_x, point_y = pygame.mouse.get_pos()
                ma_balle.dx, ma_balle.dy = obtenir_direction_vers_point(point_x, point_y)
                nbr_coups += 1

    if ma_balle.hitbox_balle.colliderect(drapeau.hitbox_trou) and ma_balle.dx**2 < 2.5 and ma_balle.dy**2 < 2.5 :
        print("Bravo", pseudo,"! Vous avez réussi en touchant la paroi  " + str(touche_paroi) + " fois ! Et en " + str(nbr_coups-1) + " coups ! BEAU SWING !")
        #best_score.append(nbr_coups)
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

