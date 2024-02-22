##################################################################################################################################################
#
#                         CLASSE / OBSTACLE - JEU MINI GOLF  |  REALISE PAR KoddaZz
#                                                               ©KoddaZz
##################################################################################################################################################


import pygame
from random import randint

RAYON = 10
DIMENSION = 500

fenetre = pygame.display.set_mode((DIMENSION, DIMENSION))
fenetre.fill([0, 0, 0])


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