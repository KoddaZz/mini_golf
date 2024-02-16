import pygame
import pygame_menu
from pygame_menu.widgets.core.widget import Widget
import pygame_menu.widgets
import pygame_menu._widgetmanager

# Initialisation de Pygame
pygame.init()

# Initialisation de la surface d'affichage
pygame.display.set_mode((400, 300))  # Ajouter cette ligne
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
pygame_menu.widgets.Button("Joueur", menu=menu_joueur)
pygame_menu.widgets.Button("Admin", menu=menu_admin)
 

# Ajout des boutons aux menus secondaires
pygame_menu.widgets.Button("Retour", menu=menu)
pygame_menu.widgets.Button("Retour", menu=menu)

# Ajout des événements aux boutons
pygame_menu.widgets.Button("Quitter", menu=close_menu)
# Boucle principale
while True:

    # Gestion des événements
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            close_menu()
        menu.update(events)

    # Affichage des menus
    menu.draw()
    pygame.display.flip()
