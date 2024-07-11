##################################################################################################################################################
#
#                         FICHIER PRINCIPAL( lancer le jeu) - JEU MINI GOLF  |  REALISE PAR KoddaZz
#                                                               ©KoddaZz
##################################################################################################################################################



import pygame
import sys
import time
from pygame.locals import *
import pygame_menu
from pygame_menu.events import CLOSE

from BookShelf import ball,barriers,hole

import register
import login
import utilities_db
#

#Initalisation des scores
touche_paroi = 0
nbr_coups = 1
LONGUEUR = 1000
LARGEUR = 500

display_surface = pygame.display.set_mode((LONGUEUR, LARGEUR))
pygame.init()

#fond = image.load('')

#Fonction permettant de gérer les déplacements de la balle
def obtenir_direction_vers_point(point_x, point_y):
    # Calcule la direction (dx, dy) vers le point (point_x, point_y)
    dx = (point_x - ma_balle.x)
    dy = (point_y - ma_balle.y)
    norme = (dx**2 + dy**2)**0.5
    if norme > 0:
        dx /= norme
        dy /= norme
    return dx*norme*0.01, dy*norme*0.01

# Fonction qui sert à determiner le parcours choisis par l'utilisateur
def parcours():
    global choix_parcours
    if choix_parcours.get_value() not in ['1','2','3']:
        choix_parcours.clear()
        menu_parcours.add.button("Inexistant !")
        menu_parcours.mainloop(display_surface)
    else:
        if choix_parcours.get_value() == '1':
            drapeau.x2 = LONGUEUR / 2
            drapeau.y2 = LARGEUR / 10
            menu_parcours.close()
        elif choix_parcours.get_value() =='2':
            drapeau.x2 = LONGUEUR / 2
            drapeau.y2 = LARGEUR / 2
            menu_parcours.close()
        else:
            drapeau.x2 = LONGUEUR * 0.90
            drapeau.y2 = LARGEUR * 0.10
            menu_parcours.close()

#Fonction qui gère quel parcours sur lequel le joueur veut jouer



ma_balle = ball.Balle() # Création de la balle de golf
drapeau = hole.LePuits() # Création du trou pour le golf

# Création des Obstacles
obstacle1 = barriers.Obstacles(50, 0, 20)
obstacle2 = barriers.Obstacles(50, 20, 20)
obstacle3 = barriers.Obstacles(50, 40, 20)
obstacle4 = barriers.Obstacles(50, 60, 20)
obstacle5 = barriers.Obstacles(50, 80, 20)
obstacle6 = barriers.Obstacles(50, 100, 20)
obstacle7 = barriers.Obstacles(50, 120, 20)
obstacle8 = barriers.Obstacles(50, 140, 20)
obstacle9 = barriers.Obstacles(50, 160, 20)
obstacles = [obstacle1,obstacle2,obstacle3,obstacle4,obstacle5,obstacle6,obstacle7,obstacle8,obstacle9]

for i in range(100):
        obstacle = barriers.Obstacles(70,0+i,20)
        
        obstacle.draw()

#Menu Principal du jeu
menu = pygame_menu.Menu(
    height=LARGEUR,
    width=LONGUEUR,
    title="Mini Golf",
    theme=pygame_menu.themes.THEME_DEFAULT,
)

#Menu Parcours
menu_parcours = pygame_menu.Menu(
    height=LARGEUR,
    width=LONGUEUR,
    title='Parcours',
    theme=pygame_menu.themes.THEME_DEFAULT,
    onclose=CLOSE,
)

#Menu du Fin du Jeu
menu_de_fin = pygame_menu.Menu(
    height=LARGEUR,
    width=LONGUEUR,
    title='Menu de Fin',
    theme=pygame_menu.themes.THEME_DEFAULT,
    onclose=CLOSE,
)

#Gesion du Menu Principal
menu.add.button("Inscription",accept_kwargs=True, action=register.menu_inscription)
menu.add.button("Connexion",accept_kwargs=True, action=login.menu_connexion)

menu.mainloop(display_surface)

# Gestion du menu "Parcours" (bouton + zone de txt)
choix_parcours = menu_parcours.add.text_input("Parcours :",default="")
menu_parcours.add.button("Jouer !", accept_kwargs=True, action=parcours)

menu_parcours.mainloop(display_surface)
fenetre = pygame.display.set_mode((LONGUEUR, LARGEUR))
fenetre.fill([51 ,153 , 0])




#Boucle qui fait tourner le jeu
while True:
    print(drapeau.x2, drapeau.y2)
    drapeau.draw()

    for obstacle in obstacles:
        obstacle.draw()
        if ma_balle.hitbox_balle.colliderect(obstacle.hitbox_obstacle): # Gestion des évènements avc les obstacles
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

    if ma_balle.y < ma_balle.taille or ma_balle.y > LARGEUR - ma_balle.taille:
            touche_paroi +=1
    if ma_balle.x < ma_balle.taille or ma_balle.x > LONGUEUR - ma_balle.taille:
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

        if register.new_user:
            print("Bravo", register.inscription_username_value.get_value(),"! Vous avez réussi en touchant la paroi  " + str(touche_paroi) + " fois ! Et en " + str(nbr_coups-1) + " coups ! BEAU SWING !")
        #best_score.append(nbr_coups)
            utilities_db.insert_data_score(register.inscription_username_value.get_value(),(nbr_coups-1))
            menu_de_fin.mainloop(display_surface)
            menu_de_fin.close()
        else:
            print("Bravo", login.username_value.get_value(),"! Vous avez réussi en touchant la paroi  " + str(touche_paroi) + " fois ! Et en " + str(nbr_coups-1) + " coups ! BEAU SWING !")
            utilities_db.insert_data_score(login.username_value.get_value(),(nbr_coups-1))
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