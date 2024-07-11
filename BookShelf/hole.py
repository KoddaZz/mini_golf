##################################################################################################################################################
#
#                         CLASSE / Trou du Golf - JEU MINI GOLF  |  REALISE PAR KoddaZz
#                                                               ©KoddaZz
##################################################################################################################################################


import pygame
LONGUEUR = 1000
LARGEUR = 500
trou = 15

fenetre = pygame.display.set_mode((LONGUEUR, LARGEUR))
fenetre.fill([0, 0, 0])

class LePuits:
    def __init__(self):
        self.x2 = 0
        self.y2 = 0
        self.color = (0, 0, 0)
        self.trou = trou
        self.hitbox_trou = pygame.Rect(self.x2, self.y2, self.trou, self.trou)

    def draw(self):
        pygame.draw.circle(fenetre, self.color, (self.x2, self.y2), self.trou)