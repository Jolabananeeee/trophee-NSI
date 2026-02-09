import pygame
import sys
import os
from menu import afficher_menu, gerer_menu

#Differents etats du jeu : menu, jeu, inventaire, parametres, credits, julien, aleksy, ivana, joe

pygame.init()

BASE_DIR = os.path.dirname(__file__)


# Constantes
LARGEUR, HAUTEUR = 800, 600
FPS = 60

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
VERT = (0, 200, 0)
ROUGE = (200, 0, 0)
GRIS = (180, 180, 180)

ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Link.exe")
clock = pygame.time.Clock()


coeur_img = pygame.image.load(
    os.path.join(BASE_DIR, "../assets/coeur_pv.png")
).convert_alpha()

coeur_img = pygame.transform.scale(coeur_img, (25, 25))

ETAT_JEU = "menu"
selection_menu = 0
selection_credits = 0

fade_alpha = 255
fade_actif = True

vie_max = 5


class Joueur:
    def __init__(self):
        self.rect = pygame.Rect(380, 280, 40, 40)
        self.vitesse = 5
        self.vies = vie_max
        self.invincible = 0

    def deplacer(self):
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT] or touches[pygame.K_q]:
            self.rect.x -= self.vitesse
        if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
            self.rect.x += self.vitesse
        if touches[pygame.K_UP] or touches[pygame.K_z]:
            self.rect.y -= self.vitesse
        if touches[pygame.K_DOWN] or touches[pygame.K_s]:
            self.rect.y += self.vitesse
        self.rect.clamp_ip(ecran.get_rect())

    def dessiner(self):
        pygame.draw.rect(ecran, VERT, self.rect)


class Ennemi:
    def __init__(self):
        self.rect = pygame.Rect(200, 150, 40, 40)
        self.vx = 3
        self.vy = 3

    def deplacer(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.left <= 0 or self.rect.right >= LARGEUR:
            self.vx = -self.vx
        if self.rect.top <= 0 or self.rect.bottom >= HAUTEUR:
            self.vy = -self.vy

    def dessiner(self):
        pygame.draw.rect(ecran, ROUGE, self.rect)


def afficher_menu():
    ecran.fill((20, 20, 20))
    font_titre = pygame.font.Font(None, 70)
    font = pygame.font.Font(None, 40)
    font_aide = pygame.font.Font(None, 22)

    titre = font_titre.render("LINK.EXE", True, BLANC)
    ecran.blit(titre, (LARGEUR // 2 - 140, 80))

    options = ["Jouer", "Paramètres", "Crédits", "Quitter"]

    for i, option in enumerate(options):
        prefixe = "> " if i == selection_menu else "  "
        couleur = BLANC if i == selection_menu else GRIS
        texte = font.render(prefixe + option, True, couleur)
        ecran.blit(texte, (LARGEUR // 2 - 120, 220 + i * 60))

    aide = font_aide.render(
        "Utilisez ↑ ↓ pour naviguer — Entrée pour sélectionner",
        True,
        GRIS
    )
    ecran.blit(aide, (LARGEUR // 2 - 190, HAUTEUR - 40))


def afficher_parametres():
    ecran.fill((10, 10, 30))
    font = pygame.font.Font(None, 40)
    ecran.blit(font.render("PARAMÈTRES", True, BLANC), (50, 50))
    ecran.blit(font.render("- Son : ON", True, GRIS), (50, 150))
    ecran.blit(font.render("- Graphismes : Normal", True, GRIS), (50, 200))
    ecran.blit(font.render("ÉCHAP : retour", True, GRIS), (50, 350))

def afficher_credits():
    ecran.fill((20, 20, 20))
    font = pygame.font.Font(None, 40)

    titre = font.render("Crédits", True, BLANC)
    ecran.blit(titre, (LARGEUR // 2 - 140, 80))

    options = ["Julien", "Aleksy", "Ivana", "Joe", "Quitter"]

    for i, option in enumerate(options):
        prefixe = "> " if i == selection_credits else "  "
        couleur = BLANC if i == selection_credits else GRIS
        texte = font.render(prefixe + option, True, couleur)
        ecran.blit(texte, (LARGEUR // 2 - 120, 220 + i * 60))

    aide = font.render(
        "Utilisez ↑ ↓ pour naviguer — Entrée pour sélectionner",
        True,
        GRIS
    )
    ecran.blit(aide, (LARGEUR // 2 - 190, HAUTEUR - 40))


def afficher_inventaire():
    overlay = pygame.Surface((LARGEUR, HAUTEUR))
    overlay.set_alpha(200)
    overlay.fill((30, 30, 30))
    ecran.blit(overlay, (0, 0))

    font = pygame.font.Font(None, 40)
    ecran.blit(font.render("INVENTAIRE", True, BLANC), (300, 80))
    ecran.blit(font.render("- Épée", True, BLANC), (250, 180))
    ecran.blit(font.render("- Clé", True, BLANC), (250, 230))
    ecran.blit(font.render("E ou ÉCHAP : retour", True, GRIS), (220, 350))


def afficher_coeurs(joueur):
    for i in range(joueur.vies):
        ecran.blit(coeur_img, (10 + i * 30, 10))

def fade_noir(alpha):
    overlay = pygame.Surface((LARGEUR, HAUTEUR))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(alpha)
    ecran.blit(overlay, (0, 0))

def afficher_julien():
    ecran.fill((20, 20, 20))
    font = pygame.font.Font(None, 40)
    ecran.blit(font.render("Julien", True, BLANC), (50, 50))
    ecran.blit(font.render("A définir", True, GRIS), (50, 150))
    ecran.blit(font.render("ÉCHAP : retour", True, GRIS), (50, 350))

def afficher_aleksy():
    ecran.fill((20, 20, 20))
    font = pygame.font.Font(None, 40)
    ecran.blit(font.render("Aleksy", True, BLANC), (50, 50))
    ecran.blit(font.render("A définir", True, GRIS), (50, 150))
    ecran.blit(font.render("ÉCHAP : retour", True, GRIS), (50, 350))

def afficher_ivana():
    ecran.fill((20, 20, 20))
    font = pygame.font.Font(None, 40)
    ecran.blit(font.render("Ivana", True, BLANC), (50, 50))
    ecran.blit(font.render("A définir", True, GRIS), (50, 150))
    ecran.blit(font.render("ÉCHAP : retour", True, GRIS), (50, 350))

def afficher_joe():
    ecran.fill((20, 20, 20))
    font = pygame.font.Font(None, 40)
    ecran.blit(font.render("Joe", True, BLANC), (50, 50))
    ecran.blit(font.render("A définir", True, GRIS), (50, 150))
    ecran.blit(font.render("ÉCHAP : retour", True, GRIS), (50, 350))


joueur = Joueur()
ennemi = Ennemi()

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if ETAT_JEU == "menu":
                if event.key == pygame.K_UP:
                    selection_menu = (selection_menu - 1) % 4
                if event.key == pygame.K_DOWN:
                    selection_menu = (selection_menu + 1) % 4
                if event.key == pygame.K_RETURN:
                    if selection_menu == 0:
                        ETAT_JEU = "jeu"
                    elif selection_menu == 1:
                        ETAT_JEU = "parametres"
                    elif selection_menu == 2:
                        ETAT_JEU = "credits"
                    elif selection_menu == 3:
                        pygame.quit()
                        sys.exit()


            elif ETAT_JEU == "credits":
                if event.key == pygame.K_UP:
                    selection_credits = (selection_credits - 1) % 5
                if event.key == pygame.K_DOWN:
                    selection_credits = (selection_credits + 1) % 5
                if event.key == pygame.K_RETURN:
                    if selection_credits == 0:
                        ETAT_JEU = "julien"
                    elif selection_credits == 1:
                        ETAT_JEU = "aleksy"
                    elif selection_credits == 2:
                        ETAT_JEU = "ivana"
                    elif selection_credits == 3:
                        ETAT_JEU = "joe"
                    elif selection_credits == 4:
                        ETAT_JEU = "menu"

            if ETAT_JEU == "jeu" and event.key == pygame.K_e:
                ETAT_JEU = "inventaire"
            
            if event.key == pygame.K_ESCAPE and ETAT_JEU in ("parametres", "credits"):
                ETAT_JEU = "menu"
            elif event.key == pygame.K_ESCAPE and ETAT_JEU in ("julien", "aleksy", "ivana", "joe"):
                ETAT_JEU = "credits"
            elif ETAT_JEU == "inventaire" and event.key in (pygame.K_e, pygame.K_ESCAPE):
                ETAT_JEU = "jeu"

    if ETAT_JEU == "jeu":
        joueur.deplacer()
        ennemi.deplacer()

        if joueur.rect.colliderect(ennemi.rect) and joueur.invincible == 0:
            joueur.vies -= 1
            joueur.invincible = FPS

        if joueur.invincible > 0:
            joueur.invincible -= 1

        if joueur.vies <= 0:
            pygame.quit()
            sys.exit()

    if ETAT_JEU == "menu":
        afficher_menu()
        if fade_actif:
            fade_noir(fade_alpha)
            fade_alpha -= 1.5
            if fade_alpha <= 0:
                fade_alpha = 0
                fade_actif = False

    elif ETAT_JEU == "jeu":
        ecran.fill(NOIR)
        joueur.dessiner()
        ennemi.dessiner()
        afficher_coeurs(joueur)

    elif ETAT_JEU == "inventaire":
        ecran.fill(NOIR)
        joueur.dessiner()
        ennemi.dessiner()
        afficher_coeurs(joueur)
        afficher_inventaire()

    elif ETAT_JEU == "parametres":
        afficher_parametres()

    elif ETAT_JEU == "credits":
        afficher_credits()

    elif ETAT_JEU == "julien":
        afficher_julien()

    elif ETAT_JEU == "aleksy":
        afficher_aleksy()

    elif ETAT_JEU == "ivana":
        afficher_ivana()

    elif ETAT_JEU == "joe":
        afficher_joe()


    pygame.display.flip()
