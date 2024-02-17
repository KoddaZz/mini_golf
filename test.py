import pygame
import pygame_menu
from pygame_menu.widgets.core.widget import Widget
import pygame_menu.widgets
import pygame_menu._widgetmanager
import pygame_menu.events as events

# Initialisation de Pygame
pygame.init()

# Initialisation de la surface d'affichage
display_surface = pygame.display.set_mode((400, 300))
def close_menu():
    pygame.quit()
"""
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
    menu.draw(display_surface)
    pygame.display.flip()"""

menu = pygame_menu.Menu(
    height=300,
    width=400,
    title="Mini Golf",
    theme=pygame_menu.themes.THEME_DEFAULT,
)

# Create the "Connexion" menu
menu_connexion = pygame_menu.Menu(
    height=300,
    width=400,
    title="Connexion",
    theme=pygame_menu.themes.THEME_DEFAULT,
)

# Create the "Inscription" menu
menu_inscription = pygame_menu.Menu(
    height=300,
    width=400,
    title="Inscription",
    theme=pygame_menu.themes.THEME_DEFAULT,
)



def handle_connexion_click():
    # Récupération des informations de connexion
    username = menu_connexion.get_widget("Username").get_value()
    password = menu_connexion.get_widget("Password").get_value()

    # Vérification des informations d'identification (remplacez ceci par votre logique)
    if username == "admin" and password == "admin":
        # Connexion réussie
        menu_connexion.hide()
        menu_joueur.show()
    else:
        # Echec de la connexion
        menu_connexion.add.label("Echec de la connexion", color=(255, 0, 0))

def handle_inscription_click():
    # Récupération des informations d'inscription
    username = menu_inscription.get_widget("Username").get_value()
    password = menu_inscription.get_widget("Password").get_value()
    # Enregistrement de l'utilisateur (remplacez ceci par votre logique)
    # ...

    # Inscription réussie
    menu_inscription.hide()
    menu_connexion.show()
    menu_connexion.add.label("Inscription réussie", color=(0, 255, 0))

menu.add.button("Inscription",accept_kwargs=True, function=menu_inscription)
menu.add.button("Connexion",accept_kwargs=True, function=handle_connexion_click)
# Menu "Connexion"
menu_connexion.add.text_input("Username:", default="")
menu_connexion.add.text_input("Password:", password=True)
menu_connexion.add.button("Connexion", accept_kwargs=True, function=handle_connexion_click)

# Menu "Inscription"
menu_inscription.add.text_input("Username:", default="")
menu_inscription.add.text_input("Password:", password=True)
menu_inscription.add.text_input("Email:", default="")
menu_inscription.add.button("Inscription", accept_kwargs=True, function=handle_inscription_click)



while True:

    # Handle events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            close_menu()
        menu.update(events)  # Check for events within the menu

    # Draw the menu
    menu.draw(display_surface)

    # Update the display
    pygame.display.flip()