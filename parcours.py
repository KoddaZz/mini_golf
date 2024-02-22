# ##################################################################################################################################################
# #
# #                         GESTION PARCOURS - JEU MINI GOLF  |  REALISE PAR KoddaZz
# #                                                               ©KoddaZz
# ##################################################################################################################################################

# import pygame
# import pygame_menu
# from pygame_menu.events import CLOSE
# from BookShelf import hole as drapeau

# DIMENSION = 500
# display_surface = pygame.display.set_mode((DIMENSION, DIMENSION))
# pygame.init()


# #Menu Parcours
# menu_parcours = pygame_menu.Menu(
#     height=DIMENSION,
#     width=DIMENSION,
#     title='Parcours',
#     theme=pygame_menu.themes.THEME_DEFAULT,
#     onclose=CLOSE,
# )

# def parcours():
#     global choix_parcours
#     if choix_parcours.get_value() not in ['1','2','3']:
#         choix_parcours.clear()
#         menu_parcours.add.button("Inexistant !")
#         menu_parcours.mainloop(display_surface)
#     else:
#         if choix_parcours.get_value() == '1':
#             drapeau.x2 = DIMENSION / 2
#             drapeau.y2 = DIMENSION / 10
#             menu_parcours.close()
#         elif choix_parcours.get_value() =='2':
#             drapeau.x2 = DIMENSION / 2
#             drapeau.y2 = DIMENSION / 2
#             menu_parcours.close()
#         else:
#             drapeau.x2 = DIMENSION * 0.90
#             drapeau.y2 = DIMENSION * 0.10
#             menu_parcours.close()

# choix_parcours = menu_parcours.add.text_input("Parcours :",default="")
# menu_parcours.add.button("Jouer !", accept_kwargs=True, action=parcours)