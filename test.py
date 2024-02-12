import pygame
import pygame_gui

pygame.init()

# Créez une fenêtre Pygame
screen = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600))

# Créez une fenêtre de connexion
login_window = pygame_gui.elements.UIWindow(
    pygame.Rect(200, 150, 400, 300),
    manager=manager,
    window_display_title="Connexion",
)

accueil_window = pygame_gui.elements.UIWindow(
    pygame.Rect(200, 150, 400, 300),
    manager = manager,
    window_display_title="Accueil",
)

connexion_bouton_2 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(150, 150, 100, 30),
    text="Connexion",
    manager=manager,
    container=accueil_window,
)

# Ajoutez des éléments d'interface utilisateur
pseudo_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(50, 50, 300, 30),
    manager=manager,
    container=login_window,
)
mdp_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(50, 100, 300, 30),
    manager=manager,
    container=login_window,
)
connexion_bouton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(150, 150, 100, 30),
    text="Connexion",
    manager=manager,
    container=login_window,
)

# Boucle principale
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == connexion_bouton_2:
                print("Clicked")
        manager.process_events(event)

    manager.update(1 / 60)
    manager.draw_ui(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
