import pygame

options = ["Jouer", "Paramètres", "Crédits", "Quitter"]
selection = 0

def gerer_menu(event):
    global selection

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            selection = (selection - 1) % len(options)
        elif event.key == pygame.K_DOWN:
            selection = (selection + 1) % len(options)
        elif event.key == pygame.K_RETURN:
            if selection == 0:
                return "jeu"
            elif selection == 1:
                return "parametres"
            elif selection == 2:
                return "credits"
            elif selection == 3:
                return "quitter"

    return None


def afficher_menu(ecran, largeur, hauteur):
    ecran.fill((20, 20, 20))

    font_titre = pygame.font.Font(None, 70)
    font = pygame.font.Font(None, 40)
    font_aide = pygame.font.Font(None, 22)

    titre = font_titre.render("LINK.EXE", True, (255, 255, 255))
    ecran.blit(titre, (largeur // 2 - 140, 80))

    for i, option in enumerate(options):
        prefixe = "> " if i == selection else "  "
        couleur = (255, 255, 255) if i == selection else (180, 180, 180)
        texte = font.render(prefixe + option, True, couleur)
        ecran.blit(texte, (largeur // 2 - 120, 220 + i * 60))

    aide = font_aide.render(
        "Utilisez ↑ ↓ — Entrée pour sélectionner",
        True,
        (180, 180, 180)
    )
    ecran.blit(aide, (largeur // 2 - 190, hauteur - 40))
