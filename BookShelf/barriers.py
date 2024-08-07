##################################################################################################################################################
#
#                         CLASSE / Obstacles - JEU MINI GOLF  |  REALISE PAR KoddaZz
#                                                               ©KoddaZz
##################################################################################################################################################


import pygame

LONGUEUR = 1000
LARGEUR = 500

fenetre = pygame.display.set_mode((LONGUEUR, LARGEUR))
fenetre.fill([0, 0, 0])

class Obstacles:
    def __init__(self, x, y, size):
        self.position_x = x
        self.position_y = y
        self.size = size
        self.color = (255, 0, 0)
        self.hitbox_obstacle = pygame.Rect(self.position_x, self.position_y, self.size, self.size)
    def draw(self):

        pygame.draw.rect(fenetre, self.color, (self.position_x, self.position_y, self.size, self.size))
