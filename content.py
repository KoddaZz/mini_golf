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


class User:
    def __init__(self, username:str, score:int) -> None:
        self.username: str = username
        self.score:int = score

class CRUD:
    def get_user(username: str, password:str) -> User | None:
        ...
    def save_user(user:User) -> None:
        ...
"""

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     pseudo TEXT,
     password TEXT,
     score INT

)
""")
conn.commit()

pseudo = ""

"""

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



def insert_data(data):
    # Exécute la requête SQL
    cursor.execute("INSERT INTO users (pseudo, password) VALUES (:pseudo, :password);", data)
    # Valide les modifications
    conn.commit()


def accueil_joueur():
    accueil = input("Avez vous déjà joué ? ").lower() # Sert à mettre en minuscule .lower()
    assert accueil in ["oui","non"], "Répondez par oui ou par non"
    if accueil == "oui":
        connexion()
    else:
        inscription()


def connexion():
    global pseudo
    pseudo = input("Quel est votre pseudo ? ")
    existe = pseudo_existant(pseudo)
    essai = 0
    while not existe: # SI le pseudo entré n'existe pas
        print("Nom inconnu")
        pseudo = input("Quel est votre pseudo ? ")
        existe = pseudo_existant(pseudo)
        essai +=1
        if essai >= 3:
            demande_inscription = input("Vous voulez vous créez un compte ?").lower()
            assert demande_inscription in["oui","non"], "Répondez par oui ou par non"
            if demande_inscription == "oui":
                inscription()
                break
            else:
                essai = 0
                continue

    while True:
        password = input("Quel est votre mot de passe ? ")
        test_existance = "SELECT * FROM users WHERE pseudo = :pseudo AND password = :password"
        cursor.execute(test_existance, {"pseudo":pseudo, "password":password})

        # Recuperation du resultat
        resultat = cursor.fetchall()

        if len(resultat) == 0:
            print("Veuillez réessayer ! ")
            continue # Continuez la boucle while ( ne pas executer la ligne en dessous )

        print("Connexion Réussie ! :)")
        break # Permet de stopper la boucle

def inscription():
    global pseudo
    data = {}
    pseudo = input("Quel est votre pseudo ? ")

    # Vérifie si le pseudo existe déjà
    existe = pseudo_existant(pseudo)
    while existe:
        print("Ce pseudo est déjà utilisé veuillez en réutiliser un autre ! ")
        pseudo = input("Quel est votre pseudo ? ")
        existe = pseudo_existant(pseudo)
    data["pseudo"] = pseudo
    password = input("Entrez votre mot de passe ! ")
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



# TENTATIVE DE TRANSFORMATION DE La GESTION DE LA BDD -> EN COURS..
"""
class Joueur:
    def __init__(self, pseudo, password):
        self.pseudo = pseudo
        self.password = password
        self._score = None

    
    def score(self):
        return self._score

    
    def score(self, value):
        if value is None or value > self._score:
            self._score = value
            cursor.execute("UPDATE users SET score = :score WHERE pseudo = :pseudo", {"score": value, "pseudo": self.pseudo})
            conn.commit()

    
    def inscription(cls, pseudo, password):
        data = {"pseudo": pseudo, "password": password}
        insert_data(data)
        return cls(pseudo, password)

    
    def connexion(cls):
        pseudo = input("Quel est votre pseudo ? ")
        existe = pseudo_existant(pseudo)
        essai = 0
        while not existe:
            print("Nom inconnu")
            pseudo = input("Quel est votre pseudo ? ")
            existe = pseudo_existant(pseudo)
            essai += 1
            if essai >= 3:
                demande_inscription = input("Vous voulez vous créez un compte ?").lower()
                assert demande_inscription in ["oui", "non"], "Répondez par oui ou par non"
                if demande_inscription == "oui":
                    return cls.inscription(pseudo, password)
                else:
                    essai = 0
                    continue

        while True:
            password = input("Quel est votre mot de passe ? ")
            test_existance = "SELECT * FROM users WHERE pseudo = :pseudo AND password = :password"
            cursor.execute(test_existance, {"pseudo": pseudo, "password": password})

            # Recuperation du resultat
            resultat = cursor.fetchall()

            if len(resultat) == 0:
                print("Veuillez réessayer ! ")
                continue

            print("Connexion Réussie ! :)")
            break

        return cls(pseudo, password)

    def get_score(self):
        cursor.execute("SELECT score FROM users WHERE pseudo = :pseudo", {"pseudo": self.pseudo})
        result = cursor.fetchone()
        return result[0]


def pseudo_existant(pseudo):
    test_pseudo = "SELECT * FROM users WHERE pseudo = :pseudo"
    cursor.execute(test_pseudo, {"pseudo": pseudo})

    # Recuperation du resultat
    resultat = cursor.fetchall()

    if len(resultat) == 0:
        return False
    else:
        return True

def accueil_joueur():
    accueil = input("Avez vous déjà joué ? ").lower()
    assert accueil in ["oui", "non"], "Répondez par oui ou par non"
    if accueil == "oui":
        return Joueur.connexion()
    else:
        return Joueur.inscription()

class GestionnaireBaseDeDonnees:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.conn:
            self.conn.close()

    def insert_data(self, data):
        self.cursor.execute("INSERT INTO users (pseudo, password) VALUES (:pseudo, :password);", data)
        self.conn.commit()

    def pseudo_existant(self, pseudo):
        test_pseudo = "SELECT * FROM users WHERE pseudo = :pseudo"
        self.cursor.execute(test_pseudo, {"pseudo": pseudo})

        # Recuperation du resultat
        resultat = self.cursor.fetchall()

        if len(resultat) == 0:
            return False
        else:
            return True
    class Infos:
        def ask
    """


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

accueil_joueur()
while True:
    print(ma_balle.dx, ma_balle.dy)
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
        Joueur.score
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
