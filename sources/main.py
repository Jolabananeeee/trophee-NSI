import pygame
import sys

pygame.init()

# Constantes


LARGEUR = 800
HAUTEUR = 600
FPS = 60

NOIR = (0, 0, 0)
VERT = (0, 200, 0)
ROUGE = (200, 0, 0)
BLANC = (255, 255, 255)

ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Link.exe")
clock = pygame.time.Clock()

# État du jeu
ETAT_JEU = "jeu"  # "jeu" ou "inventaire"


class Joueur:
    def __init__(self):
        self.rect = pygame.Rect(380, 280, 40, 40)
        self.vitesse = 5
        self.vies = 3
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

        # Bloquer dans l'écran
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


def afficher_coeurs(joueur):
    for i in range(joueur.vies):
        coeur = pygame.Rect(10 + i * 30, 10, 20, 20)
        pygame.draw.rect(ecran, ROUGE, coeur)


def afficher_inventaire():
    overlay = pygame.Surface((LARGEUR, HAUTEUR))
    overlay.set_alpha(200)
    overlay.fill((30, 30, 30))
    ecran.blit(overlay, (0, 0))

    font_titre = pygame.font.Font(None, 50)
    font_txt = pygame.font.Font(None, 30)

    titre = font_titre.render("INVENTAIRE", True, BLANC)
    ecran.blit(titre, (LARGEUR // 2 - 120, 60))

    ecran.blit(font_txt.render("- Sword", True, BLANC), (200, 160))
    ecran.blit(font_txt.render("- Key", True, BLANC), (200, 210))
    ecran.blit(font_txt.render("- Health Potion", True, BLANC), (200, 260))

    ecran.blit(font_txt.render("E ou ÉCHAP pour revenir", True, BLANC), (200, 350))


joueur = Joueur()
ennemi = Ennemi()

# Boucle principale
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                ETAT_JEU = "inventaire" if ETAT_JEU == "jeu" else "jeu"

            if event.key == pygame.K_ESCAPE and ETAT_JEU == "inventaire":
                ETAT_JEU = "jeu"

    # Mise à jour UNIQUEMENT si on est dans le jeu
    if ETAT_JEU == "jeu":
        joueur.deplacer()
        ennemi.deplacer()

        if joueur.rect.colliderect(ennemi.rect) and joueur.invincible == 0:
            joueur.vies -= 1
            joueur.invincible = FPS
            print("Aïe ! Vie restante :", joueur.vies)

        if joueur.invincible > 0:
            joueur.invincible -= 1

        if joueur.vies <= 0:
            print("GAME OVER")
            pygame.quit()
            sys.exit()

    # Affichage
    ecran.fill(NOIR)
    joueur.dessiner()
    ennemi.dessiner()
    afficher_coeurs(joueur)

    if ETAT_JEU == "inventaire":
        afficher_inventaire()

    pygame.display.flip()
