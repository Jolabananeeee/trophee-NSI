import pygame
import sys
import os

try:
    from menu import afficher_menu, gerer_menu
except ImportError:
    pass

pygame.init()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LARGEUR, HAUTEUR = 800, 600
FPS = 60

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
VERT = (0, 200, 0)
ROUGE = (200, 0, 0)
GRIS = (180, 180, 180)
BLEU_NUIT = (10, 10, 30)
JAUNE = (1, 54, 78)

ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Link.exe")
clock = pygame.time.Clock()

# --- CONFIGURATION ---
CONFIG_TOUCHES = {
    "HAUT": pygame.K_UP,
    "BAS": pygame.K_DOWN,
    "GAUCHE": pygame.K_LEFT,
    "DROITE": pygame.K_RIGHT,
    "CONFIRMER": pygame.K_z,
    "ANNULER": pygame.K_x,
    "COURIR": pygame.K_LSHIFT,
    "TOUCHER": pygame.K_a
}

CONFIG_JEU = {
    "SON": True,
    "GRAPHISMES": "NORMAL"
}

# --- CHARGEMENT ---
def charger_image(chemin, taille=None, transparence=True):
    full_path = os.path.join(BASE_DIR, chemin)
    try:
        if transparence:
            img = pygame.image.load(full_path).convert_alpha()
        else:
            img = pygame.image.load(full_path).convert()
        if taille:
            img = pygame.transform.scale(img, taille)
        return img
    except FileNotFoundError:
        surf = pygame.Surface(taille if taille else (40, 40))
        surf.fill(ROUGE)
        return surf

def charger_police(taille):
    chemin_police = os.path.join(BASE_DIR, "assets", "OMORI_GAME.ttf")
    try:
        return pygame.font.Font(chemin_police, taille)
    except FileNotFoundError:
        return pygame.font.Font(None, taille)

# --- ASSETS ---
coeur_img = charger_image("assets/coeur_pv.png", (25, 25), transparence=True)
titre_img = charger_image("assets/titre.png", taille=(300, 100), transparence=True) 
bg1 = charger_image("assets/bg1.png", (LARGEUR, HAUTEUR), transparence=False)
bg2 = charger_image("assets/bg2.png", (LARGEUR, HAUTEUR), transparence=False)
img_main = charger_image("assets/main.png", (25, 20), transparence=True)

liste_fonds = [bg1, bg2]
index_bg_actuel = 0
dernier_changement_bg = 0
DELAI_CHANGEMENT = 5000 

police_titre_texte = charger_police(50)
police_bouton = charger_police(32)
police_texte = charger_police(24)
police_aide = charger_police(20)

# --- ETATS ---
ETAT_JEU = "menu"
selection_menu = 0
selection_credits = 0
selection_fichier = 0 
selection_game_over = 0 # Pour le menu de mort
fade_alpha = 255
fade_actif = True
vie_max = 5

# --- PARAMETRES ---
onglet_actif = 0
selection_parametre = 0
en_attente_touche = False
cle_a_modifier = None

# --- CREATION OBJETS (DICTIONNAIRES) ---

def creer_joueur():
    return {
        "rect": pygame.Rect(380, 280, 40, 40),
        "vitesse": 5,
        "vies": vie_max,
        "invincible": 0
    }

def deplacer_joueur(joueur):
    touches = pygame.key.get_pressed()
    dx, dy = 0, 0
    
    if touches[CONFIG_TOUCHES["GAUCHE"]]: dx = -joueur["vitesse"]
    if touches[CONFIG_TOUCHES["DROITE"]]: dx = joueur["vitesse"]
    if touches[CONFIG_TOUCHES["HAUT"]]: dy = -joueur["vitesse"]
    if touches[CONFIG_TOUCHES["BAS"]]: dy = joueur["vitesse"]
    
    if touches[CONFIG_TOUCHES["COURIR"]]:
        joueur["rect"].x += dx * 2
        joueur["rect"].y += dy * 2
    else:
        joueur["rect"].x += dx
        joueur["rect"].y += dy
        
    joueur["rect"].clamp_ip(ecran.get_rect())

def dessiner_joueur(joueur):
    pygame.draw.rect(ecran, VERT, joueur["rect"])


def creer_ennemi():
    return {
        "rect": pygame.Rect(200, 150, 40, 40),
        "vx": 3,
        "vy": 3
    }

def deplacer_ennemi(ennemi):
    ennemi["rect"].x += ennemi["vx"]
    ennemi["rect"].y += ennemi["vy"]
    
    if ennemi["rect"].left <= 0 or ennemi["rect"].right >= LARGEUR:
        ennemi["vx"] = -ennemi["vx"]
    if ennemi["rect"].top <= 0 or ennemi["rect"].bottom >= HAUTEUR:
        ennemi["vy"] = -ennemi["vy"]

def dessiner_ennemi(ennemi):
    pygame.draw.rect(ecran, ROUGE, ennemi["rect"])

# --- AFFICHAGE ---

def afficher_menu_local():
    global index_bg_actuel, dernier_changement_bg
    temps_actuel = pygame.time.get_ticks()
    if temps_actuel - dernier_changement_bg > DELAI_CHANGEMENT:
        index_bg_actuel = (index_bg_actuel + 1) % len(liste_fonds)
        dernier_changement_bg = temps_actuel

    ecran.blit(liste_fonds[index_bg_actuel], (0, 0))
    overlay = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    ecran.blit(overlay, (0, 0))
    
    titre_rect = titre_img.get_rect(center=(LARGEUR // 2, HAUTEUR // 6))
    ecran.blit(titre_img, titre_rect)

    options = ["JOUER", "PARAMÈTRES", "CRÉDITS", "QUITTER"]
    bouton_largeur, bouton_hauteur, espacement = 180, 40, 15
    start_x = (LARGEUR - (len(options) * bouton_largeur + (len(options) - 1) * espacement)) // 2
    y_pos = HAUTEUR - 100

    for i, option in enumerate(options):
        x_pos = start_x + i * (bouton_largeur + espacement)
        bouton_rect = pygame.Rect(x_pos, y_pos, bouton_largeur, bouton_hauteur)
        epaisseur = 3 if i == selection_menu else 1
        pygame.draw.rect(ecran, NOIR, bouton_rect)
        pygame.draw.rect(ecran, BLANC, bouton_rect, epaisseur)
        texte_surface = police_bouton.render(option, True, BLANC)
        ecran.blit(texte_surface, texte_surface.get_rect(center=bouton_rect.center))
    
    nom_touche = pygame.key.name(CONFIG_TOUCHES['CONFIRMER']).upper()
    aide_surface = police_aide.render(f"FLÈCHES : naviguer — {nom_touche} : sélectionner", True, GRIS)
    ecran.blit(aide_surface, aide_surface.get_rect(center=(LARGEUR // 2, HAUTEUR - 30)))

def afficher_selection_fichier():
    ecran.fill(NOIR)
    slot_largeur, slot_hauteur = 600, 140
    start_x = (LARGEUR - slot_largeur) // 2
    start_y, espacement = 50, 20

    for i in range(3):
        y_pos = start_y + i * (slot_hauteur + espacement)
        rect_slot = pygame.Rect(start_x, y_pos, slot_largeur, slot_hauteur)
        epaisseur = 4 if i == selection_fichier else 2
        couleur_bord = BLANC if i == selection_fichier else GRIS
        
        pygame.draw.rect(ecran, NOIR, rect_slot)
        pygame.draw.rect(ecran, couleur_bord, rect_slot, epaisseur)
        ecran.blit(police_bouton.render(f"FICHIER {i + 1}", True, BLANC), (rect_slot.x + 15, rect_slot.y + 10))
        
        ligne_y = rect_slot.y + 45
        pygame.draw.line(ecran, couleur_bord, (rect_slot.x, ligne_y), (rect_slot.right, ligne_y), 2)
        ligne_x = rect_slot.x + 130
        pygame.draw.line(ecran, couleur_bord, (ligne_x, ligne_y), (ligne_x, rect_slot.bottom), 2)
        
        y_ligne1 = ligne_y + 32
        pygame.draw.line(ecran, couleur_bord, (ligne_x, y_ligne1), (rect_slot.right, y_ligne1), 1)
        y_ligne2 = y_ligne1 + 32
        pygame.draw.line(ecran, couleur_bord, (ligne_x, y_ligne2), (rect_slot.right, y_ligne2), 1)

    nom_touche = pygame.key.name(CONFIG_TOUCHES['CONFIRMER']).upper()
    nom_retour = pygame.key.name(CONFIG_TOUCHES['ANNULER']).upper()
    txt_aide = police_aide.render(f"{nom_touche} : CHARGER — {nom_retour} : RETOUR", True, GRIS)
    ecran.blit(txt_aide, txt_aide.get_rect(center=(LARGEUR // 2, HAUTEUR - 30)))

def dessiner_touche(x, y, texte, couleur=BLANC, est_selectionne=False):
    surf = police_texte.render(texte, True, couleur)
    rect = surf.get_rect(center=(x, y))
    taille_min = 34
    largeur_box = max(taille_min, rect.width + 12)
    box_rect = pygame.Rect(0, 0, largeur_box, taille_min)
    box_rect.center = (x, y)
    
    if est_selectionne and en_attente_touche:
        pygame.draw.rect(ecran, ROUGE, box_rect)
        pygame.draw.rect(ecran, BLANC, box_rect, 2)
    else:
        pygame.draw.rect(ecran, NOIR, box_rect)
        pygame.draw.rect(ecran, couleur, box_rect, 2)
        
    ecran.blit(surf, rect)

def afficher_parametres():
    ecran.fill(NOIR)
    y_header = 60
    pygame.draw.line(ecran, BLANC, (50, y_header - 25), (LARGEUR - 50, y_header - 25), 3)
    
    onglets = ["GÉNÉRAL", "AUDIO", "CONTRÔLES", "SYSTÈME"]
    largeur_onglets = 600 
    x_start = (LARGEUR - largeur_onglets) // 2 + 50
    x_step = 160 
    
    for i, onglet in enumerate(onglets):
        couleur = ROUGE if i == onglet_actif else BLANC
        txt = police_bouton.render(onglet, True, couleur)
        rect = txt.get_rect(center=(x_start + i * x_step, y_header))
        ecran.blit(txt, rect)
        
        if i == onglet_actif:
             main_rect = img_main.get_rect(midright=(rect.left - 10, rect.centery))
             ecran.blit(img_main, main_rect)

    pygame.draw.line(ecran, BLANC, (50, y_header + 25), (LARGEUR - 50, y_header + 25), 3)

    start_y = 160
    line_height = 45

    if onglet_actif == 2: # CONTRÔLES
        ecran.blit(police_bouton.render("CLAVIER", True, BLANC), (380, 130))
        ecran.blit(police_bouton.render("MANETTE", True, BLANC), (600, 130))
        
        ordre_affichage = ["HAUT", "BAS", "GAUCHE", "DROITE", "CONFIRMER", "ANNULER", "COURIR", "TOUCHER"]
        
        for i, action in enumerate(ordre_affichage):
            y = 190 + i * line_height
            est_selectionne = (i == selection_parametre)
            couleur_texte = ROUGE if est_selectionne else BLANC
            
            txt_action = police_texte.render(action, True, couleur_texte)
            ecran.blit(txt_action, (80, y - 12))
            
            if est_selectionne:
                main_rect = img_main.get_rect(midright=(70, y - 12 + 10))
                ecran.blit(img_main, main_rect)

            code_touche = CONFIG_TOUCHES[action]
            nom_touche = pygame.key.name(code_touche).upper()
            
            if est_selectionne and en_attente_touche:
                texte_touche = "..." 
            else:
                texte_touche = nom_touche

            dessiner_touche(430, y, texte_touche, couleur_texte, est_selectionne)
            dessiner_touche(660, y, "-", GRIS)

    elif onglet_actif == 0: # GÉNÉRAL
        options = ["GRAPHISMES"]
        for i, opt in enumerate(options):
            y = start_y + i * line_height
            couleur = ROUGE if i == selection_parametre else BLANC
            ecran.blit(police_texte.render(f"{opt} : {CONFIG_JEU['GRAPHISMES']}", True, couleur), (100, y))
            if i == selection_parametre:
                ecran.blit(img_main, (70, y))

    elif onglet_actif == 1: # AUDIO
        options = ["SON"]
        for i, opt in enumerate(options):
            y = start_y + i * line_height
            couleur = ROUGE if i == selection_parametre else BLANC
            etat = "ON" if CONFIG_JEU['SON'] else "OFF"
            ecran.blit(police_texte.render(f"{opt} : {etat}", True, couleur), (100, y))
            if i == selection_parametre:
                ecran.blit(img_main, (70, y))
                
    elif onglet_actif == 3: # SYSTÈME
        ecran.blit(police_texte.render("Version 1.0.8", True, GRIS), (100, start_y))

    pygame.draw.line(ecran, BLANC, (50, HAUTEUR - 60), (LARGEUR - 50, HAUTEUR - 60), 3)
    nom_retour = pygame.key.name(CONFIG_TOUCHES['ANNULER']).upper()
    aide = police_aide.render(f"{nom_retour} : RETOUR", True, GRIS)
    ecran.blit(aide, aide.get_rect(center=(LARGEUR//2, HAUTEUR - 30)))

def afficher_credits():
    ecran.fill((20, 20, 20))
    titre = police_titre_texte.render("Crédits", True, BLANC)
    ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2, 80)))
    options = ["Julien", "Aleksy", "Ivana", "Joe", "Quitter"]
    for i, option in enumerate(options):
        couleur = BLANC if i == selection_credits else GRIS
        txt = police_bouton.render(("> " if i == selection_credits else "  ") + option, True, couleur)
        ecran.blit(txt, txt.get_rect(center=(LARGEUR // 2, 220 + i * 60)))
    
    nom_touche = pygame.key.name(CONFIG_TOUCHES['CONFIRMER']).upper()
    aide_surface = police_aide.render(f"FLÈCHES : naviguer — {nom_touche} : sélectionner", True, GRIS)
    ecran.blit(aide_surface, aide_surface.get_rect(center=(LARGEUR // 2, HAUTEUR - 40)))

def afficher_inventaire():
    overlay = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
    overlay.fill((30, 30, 30, 200))
    ecran.blit(overlay, (0, 0))
    ecran.blit(police_titre_texte.render("INVENTAIRE", True, BLANC), (300, 80))
    ecran.blit(police_texte.render("- Épée", True, BLANC), (250, 180))
    ecran.blit(police_texte.render("- Clé", True, BLANC), (250, 230))
    nom_retour = pygame.key.name(CONFIG_TOUCHES['ANNULER']).upper()
    ecran.blit(police_aide.render(f"{nom_retour} : retour", True, GRIS), (220, 350))

# --- NOUVEAU : MENU DE MORT ---
def afficher_game_over():
    ecran.fill(NOIR)
    
    txt_mort = police_titre_texte.render("VOUS AVEZ SUCCOMBÉ...", True, ROUGE)
    ecran.blit(txt_mort, txt_mort.get_rect(center=(LARGEUR // 2, HAUTEUR // 3)))
    
    options = ["RÉAPPARAÎTRE", "REVENIR AU MENU"]
    
    for i, option in enumerate(options):
        couleur = BLANC if i == selection_game_over else GRIS
        txt = police_bouton.render(option, True, couleur)
        rect = txt.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 50 + i * 60))
        
        if i == selection_game_over:
            # Cadre + main
            border_rect = rect.inflate(20, 10)
            pygame.draw.rect(ecran, NOIR, border_rect)
            pygame.draw.rect(ecran, BLANC, border_rect, 2)
            ecran.blit(img_main, img_main.get_rect(midright=(border_rect.left - 10, border_rect.centery)))
            
        ecran.blit(txt, rect)

def afficher_coeurs(joueur_data):
    for i in range(joueur_data["vies"]):
        ecran.blit(coeur_img, (10 + i * 30, 10))

def fade_noir(alpha):
    overlay = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, int(alpha)))
    ecran.blit(overlay, (0, 0))

def afficher_personne(nom, role):
    ecran.fill((20, 20, 20))
    ecran.blit(police_titre_texte.render(nom, True, BLANC), (50, 50))
    ecran.blit(police_texte.render(role, True, GRIS), (50, 150))
    nom_retour = pygame.key.name(CONFIG_TOUCHES['ANNULER']).upper()
    ecran.blit(police_aide.render(f"{nom_retour} : retour", True, GRIS), (50, 350))

# --- INITIALISATION OBJETS ---
joueur = creer_joueur()
ennemi = creer_ennemi()

# --- BOUCLE PRINCIPALE ---
while True:
    clock.tick(FPS)
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # REBINDING
        if ETAT_JEU == "parametres" and en_attente_touche:
            if event.type == pygame.KEYDOWN:
                CONFIG_TOUCHES[cle_a_modifier] = event.key
                en_attente_touche = False
                cle_a_modifier = None
            continue

        # NAVIGATION
        if event.type == pygame.KEYDOWN:
            if ETAT_JEU == "menu":
                if event.key == pygame.K_LEFT: selection_menu = (selection_menu - 1) % 4
                if event.key == pygame.K_RIGHT: selection_menu = (selection_menu + 1) % 4
                if event.key == CONFIG_TOUCHES["CONFIRMER"]:
                    if selection_menu == 0: ETAT_JEU = "selection_fichier"
                    elif selection_menu == 1: 
                        ETAT_JEU = "parametres"
                        onglet_actif = 0
                        selection_parametre = 0
                    elif selection_menu == 2: ETAT_JEU = "credits"
                    elif selection_menu == 3: pygame.quit(); sys.exit()

            elif ETAT_JEU == "parametres":
                if event.key == pygame.K_LEFT: 
                    onglet_actif = (onglet_actif - 1) % 4
                    selection_parametre = 0
                if event.key == pygame.K_RIGHT: 
                    onglet_actif = (onglet_actif + 1) % 4
                    selection_parametre = 0

                nb_items = 0
                if onglet_actif == 2: nb_items = 8
                elif onglet_actif == 0: nb_items = 1
                elif onglet_actif == 1: nb_items = 1
                
                if nb_items > 0:
                    if event.key == pygame.K_UP: selection_parametre = (selection_parametre - 1) % nb_items
                    if event.key == pygame.K_DOWN: selection_parametre = (selection_parametre + 1) % nb_items

                if event.key == CONFIG_TOUCHES["CONFIRMER"]:
                    if onglet_actif == 2:
                        ordre = ["HAUT", "BAS", "GAUCHE", "DROITE", "CONFIRMER", "ANNULER", "COURIR", "TOUCHER"]
                        cle_a_modifier = ordre[selection_parametre]
                        en_attente_touche = True
                    elif onglet_actif == 1: CONFIG_JEU["SON"] = not CONFIG_JEU["SON"]
                    elif onglet_actif == 0:
                        modes = ["BAS", "NORMAL", "HAUT"]
                        curr = modes.index(CONFIG_JEU["GRAPHISMES"])
                        CONFIG_JEU["GRAPHISMES"] = modes[(curr + 1) % 3]

                if event.key == CONFIG_TOUCHES["ANNULER"] or event.key == pygame.K_ESCAPE:
                    ETAT_JEU = "menu"

            elif ETAT_JEU == "selection_fichier":
                if event.key == pygame.K_UP: selection_fichier = (selection_fichier - 1) % 3
                if event.key == pygame.K_DOWN: selection_fichier = (selection_fichier + 1) % 3
                if event.key == CONFIG_TOUCHES["CONFIRMER"]: ETAT_JEU = "jeu"
                if event.key == CONFIG_TOUCHES["ANNULER"] or event.key == pygame.K_ESCAPE: ETAT_JEU = "menu"

            elif ETAT_JEU == "jeu":
                if event.key == pygame.K_e: ETAT_JEU = "inventaire"
                elif event.key == CONFIG_TOUCHES["ANNULER"] or event.key == pygame.K_ESCAPE: ETAT_JEU = "menu"

            elif ETAT_JEU == "inventaire":
                if event.key in (pygame.K_e, CONFIG_TOUCHES["ANNULER"], pygame.K_ESCAPE): ETAT_JEU = "jeu"

            elif ETAT_JEU == "credits":
                if event.key == pygame.K_UP: selection_credits = (selection_credits - 1) % 5
                if event.key == pygame.K_DOWN: selection_credits = (selection_credits + 1) % 5
                if event.key == CONFIG_TOUCHES["CONFIRMER"]:
                    etats = ["julien", "aleksy", "ivana", "joe", "menu"]
                    ETAT_JEU = etats[selection_credits]
                if event.key == CONFIG_TOUCHES["ANNULER"] or event.key == pygame.K_ESCAPE: ETAT_JEU = "menu"

            elif ETAT_JEU in ("julien", "aleksy", "ivana", "joe"):
                if event.key == CONFIG_TOUCHES["ANNULER"] or event.key == pygame.K_ESCAPE: ETAT_JEU = "credits"

            # --- GESTION INPUT GAME OVER ---
            elif ETAT_JEU == "game_over":
                if event.key == pygame.K_UP:
                    selection_game_over = (selection_game_over - 1) % 2
                if event.key == pygame.K_DOWN:
                    selection_game_over = (selection_game_over + 1) % 2
                
                if event.key == CONFIG_TOUCHES["CONFIRMER"]:
                    if selection_game_over == 0: # RÉAPPARAÎTRE
                        joueur["vies"] = vie_max
                        joueur["rect"].topleft = (380, 280)
                        joueur["invincible"] = FPS * 2
                        ETAT_JEU = "jeu"
                    elif selection_game_over == 1: # REVENIR AU MENU
                        joueur["vies"] = vie_max
                        joueur["rect"].topleft = (380, 280)
                        ETAT_JEU = "menu"

    # --- LOGIQUE ---
    if ETAT_JEU == "jeu":
        deplacer_joueur(joueur)
        deplacer_ennemi(ennemi)
        if joueur["rect"].colliderect(ennemi["rect"]) and joueur["invincible"] == 0:
            joueur["vies"] -= 1
            joueur["invincible"] = FPS
        if joueur["invincible"] > 0: joueur["invincible"] -= 1
        
        # MORT : Passage à l'état game_over
        if joueur["vies"] <= 0:
            ETAT_JEU = "game_over"

    # --- AFFICHAGE ---
    if ETAT_JEU == "menu":
        afficher_menu_local()
        if fade_actif:
            fade_noir(fade_alpha)
            fade_alpha -= 1.5
            if fade_alpha <= 0: fade_actif = False

    elif ETAT_JEU == "selection_fichier": afficher_selection_fichier()
    
    elif ETAT_JEU == "jeu":
        ecran.fill(NOIR)
        dessiner_joueur(joueur)
        dessiner_ennemi(ennemi)
        afficher_coeurs(joueur)
        
    elif ETAT_JEU == "inventaire":
        ecran.fill(NOIR)
        dessiner_joueur(joueur)
        dessiner_ennemi(ennemi)
        afficher_coeurs(joueur)
        afficher_inventaire()
        
    elif ETAT_JEU == "parametres": afficher_parametres()
    elif ETAT_JEU == "credits": afficher_credits()
    elif ETAT_JEU == "game_over": afficher_game_over() # Appel de la fonction
    elif ETAT_JEU == "julien": afficher_personne("Julien", "Développeur")
    elif ETAT_JEU == "aleksy": afficher_personne("Aleksy", "Graphiste")
    elif ETAT_JEU == "ivana": afficher_personne("Ivana", "Testeur")
    elif ETAT_JEU == "joe": afficher_personne("Joe", "Support")

    pygame.display.flip()
    