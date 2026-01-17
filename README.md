# version 0.0.0.1   
n'inclue pas de dossiers personel exemple (video de parent) 
         






#import pygame
import os
import sys
import random
import math

# --- CONFIGURATION ---
TITRE_MENU = "Elias apprend son ABC"
CHEMIN_IMAGES = "assets/images"  # Utilisé seulement pour les objets (chat, ballon...)
COULEURS_FONDS = [(255, 87, 51), (51, 255, 87), (51, 87, 255), (255, 195, 0), (199, 0, 57)]

IMAGIER = {
    'a': 'ABEILLE', 'b': 'BALLON', 'c': 'CHAT', 'd': 'DAUPHIN', 'e': 'ELEPHANT',
    'f': 'FLEUR', 'g': 'GATEAU', 'h': 'HIBOU', 'i': 'ILE', 'j': 'JOUET',
    'k': 'KANGOUROU', 'l': 'LION', 'm': 'MAMAN', 'n': 'NUAGE', 'o': 'OISEAU',
    'p': 'PAPA', 'q': 'QUILLE', 'r': 'ROBOT', 's': 'SOLEIL', 't': 'TRAIN',
    'u': 'UNIVERS', 'v': 'VACHE', 'w': 'WAGON', 'x': 'XYLOPHONE', 'y': 'YAOURT', 'z': 'ZEBRE'
}


class JeuElias:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.w, self.h = self.screen.get_size()
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()

        # POLICES IDENTIQUES
        # La lettre au centre est très grosse, le mot en bas est moyen
        self.font_geante = pygame.font.SysFont("Arial", int(self.h * 0.6), bold=True)
        self.font_mot = pygame.font.SysFont("Arial", int(self.h * 0.12), bold=True)
        self.font_menu = pygame.font.SysFont("Comic Sans MS", 80, bold=True)

        self.surface_centre = None
        self.mot_actuel = ""
        self.lettre_actuelle = ""
        self.couleur_fond = (25, 25, 112)
        self.etat = "MENU"
        self.running = True
        self.anim_timer = 0

    def charger_touche(self, lettre):
        """Prépare la lettre centrale et le mot du bas."""
        self.lettre_actuelle = lettre.upper()
        self.mot_actuel = IMAGIER.get(lettre, self.lettre_actuelle)

        # On crée la surface de la lettre géante (Texte au lieu d'image)
        self.surface_centre = self.font_geante.render(self.lettre_actuelle, True, (255, 255, 255))
        self.rect_centre = self.surface_centre.get_rect(center=(self.w // 2, self.h // 2 - 50))

        self.couleur_fond = random.choice(COULEURS_FONDS)
        self.anim_timer = 0

    def dessiner_texte_avec_ombre(self, texte, font, centre_y, couleur=(255, 255, 255)):
        """Utilitaire pour dessiner du texte blanc avec une ombre noire."""
        surface = font.render(texte, True, couleur)
        ombre = font.render(texte, True, (0, 0, 0))
        rect = surface.get_rect(center=(self.w // 2, centre_y))

        # On dessine l'ombre décalée de 5 pixels
        self.screen.blit(ombre, rect.move(5, 5))
        self.screen.blit(surface, rect)

    def dessiner_jeu(self):
        self.screen.fill(self.couleur_fond)

        if self.lettre_actuelle:
            # 1. Lettre géante au centre
            self.dessiner_texte_avec_ombre(self.lettre_actuelle, self.font_geante, self.h // 2 - 50)

            # 2. Mot animé en bas
            offset_y = math.sin(self.anim_timer * 0.08) * 10
            self.dessiner_texte_avec_ombre(self.mot_actuel, self.font_mot, self.h - 150 + offset_y)

            self.anim_timer += 1

    def boucle(self):
        while self.running:
            if self.etat == "MENU":
                self.screen.fill((25, 25, 112))
                self.dessiner_texte_avec_ombre(TITRE_MENU, self.font_menu, self.h // 2, (255, 215, 0))
            else:
                self.dessiner_jeu()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif self.etat == "MENU":
                        self.etat = "JEU"
                    else:
                        touche = pygame.key.name(event.key).lower()
                        if len(touche) == 1 and touche.isalnum():
                            self.charger_touche(touche)

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    JeuElias().boucle()# Un-jeux-ducatif-
