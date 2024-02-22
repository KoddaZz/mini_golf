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

#Initalisation des scores
touche_paroi = 0
nbr_coups = 1
DIMENSION = 500
new_user = False #-> Permet de faire la différence entre un nouvel utilisateur ou un ancien ( connexion / inscription )

display_surface = pygame.display.set_mode((DIMENSION, DIMENSION))
pygame.init()


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



ma_balle = ball.Balle() # Création de la balle de golf
drapeau = hole.LePuits() # Création du trou pour le golf

# Création des Obstacles
obstacle1 = barriers.Obstacles(200, 200, 20)
obstacle2 = barriers.Obstacles(300, 300, 30)

obstacles = [obstacle1,obstacle2]

for obstacle in obstacles:
        obstacle.draw()

#Menu Principal du jeu

menu = pygame_menu.Menu(
    height=DIMENSION,
    width=DIMENSION,
    title="Mini Golf",
    theme=pygame_menu.themes.THEME_DEFAULT,
)

menu_de_fin = pygame_menu.Menu(
    height=DIMENSION,
    width=DIMENSION,
    title='Menu de Fin',
    theme=pygame_menu.themes.THEME_DEFAULT,
    onclose=CLOSE,
)


menu.add.button("Inscription",accept_kwargs=True, action=register.menu_inscription)
menu.add.button("Connexion",accept_kwargs=True, action=login.menu_connexion)

menu.mainloop(display_surface)



fenetre = pygame.display.set_mode((DIMENSION, DIMENSION))
fenetre.fill([51 ,153 , 0])
#Boucle qui fait tourner le jeu
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