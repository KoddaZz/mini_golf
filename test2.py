import pygame
import pygame_menu
from pygame_menu.widgets.core.widget import Widget
import pygame_menu.widgets
import pygame_menu._widgetmanager
from pygame_menu.events import BACK, CLOSE, EXIT

# Initialisation de Pygame
pygame.init()

# Initialisation de la surface d'affichage
surface = pygame.display.set_mode((400, 300))


def close_menu():
    pygame.quit()

# Création du menu
menu = pygame_menu.Menu(
    height=300,
    width=400,
    title="Inscription",
    theme=pygame_menu.themes.THEME_DEFAULT,
)


menu_joueur = pygame_menu.Menu(
    height=300,
    width=400,
    title="Menu Joueur",
    theme=pygame_menu.themes.THEME_DEFAULT,
)
menu_admin = pygame_menu.Menu(     
    height=300,
    width=400,
    title="Menu Admin",
    theme=pygame_menu.themes.THEME_DEFAULT,
)

# Ajout des widgets au menu d'inscription
menu.add.text_input("Nom d'utilisateur:", default="")
menu.add.text_input("Mot de passe:", password=True)
menu.add.button("Joueur", action=menu_joueur)
menu.add.button("Admin", action=menu_admin)
# Ajout des événements aux boutons
menu.add.button("Quitter", action=EXIT)
 

# Ajout des boutons aux menus secondaires
menu_joueur.add.button("Retour", action=BACK)
menu_admin.add.button("Retour", action=BACK)

menu.mainloop(surface)