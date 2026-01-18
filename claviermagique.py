import os
import sys
import pygame
import random
import math
import threading
import time
import speech_recognition as sr
import subprocess

# --- PREPARATION DU MOTEUR ---
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

COULEURS = {
    "fond": (245, 250, 255),
    "texte_fonce": (60, 70, 90),
    "jaune_etoile": (255, 215, 100),
    "violet_clair": (150, 160, 200),
    "rose": (255, 150, 180),
    "vert_succes": (100, 200, 140),
    "gris_lettre": (230, 235, 245)
}

# les mots (sans accents)
DICTIONNAIRE = {
    'a': 'AVION', 'b': 'BALLE', 'c': 'CHAT', 'd': 'DODO', 'e': 'EAU',
    'f': 'FLEUR', 'h': 'HIBOU', 'i': 'IGLOO', 'j': 'JOUET', 'k': 'KIWI',
    'l': 'LUNE', 'm': 'MAMAN', 'n': 'NUAGE', 'o': 'OURS', 'p': 'PAPA',
    'q': 'QUILLE', 'r': 'ROBOT', 's': 'SOLEIL', 't': 'TRAIN', 'u': 'UN',
    'v': 'VACHE', 'w': 'WAGON', 'x': 'XYLOPHONE', 'y': 'YOYO', 'z': 'ZEBRE'
}


class Particule:
    """des esti de tbk de confetti"""

    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.vitesse_x = random.uniform(-7, 7)
        self.vitesse_y = random.uniform(-12, -4)
        self.vie = 1.0
        self.couleur = couleur
        self.taille = random.randint(4, 12)

    def bouger(self):
        self.x += self.vitesse_x
        self.y += self.vitesse_y
        self.vitesse_y += 0.4  # La gravité des particule (confetti I guess
        self.vie -= 0.02


class JeuElias:
    def __init__(self):
        # Configuration de la fenêtre
        self.fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.largeur, self.hauteur = self.fenetre.get_size()
        pygame.mouse.set_visible(False)
        self.horloge = pygame.time.Clock()

        # Fichiers
        self.fichier_video = "assets/videos/surprise.mp4"
        self.fichier_record_m1 = "record_m1.txt"
        self.fichier_record_m2 = "record_m2.txt"

        # Etats du jeu
        self.endroit_du_jeu = "MENU"  # MENU ou JOUER
        self.numero_module = 1
        self.record_module1 = self.lire_le_record(self.fichier_record_m1)
        self.record_module2 = self.lire_le_record(self.fichier_record_m2)

        
        self.moment_du_depart = 0
        self.mot_actuel = ""
        self.lettres_deja_tapees = ""
        self.touche_a_trouver = ""
        self.derniere_touche = ""
        self.liste_particules = []
        self.message_bravo = ""
        self.chrono_message = 0
        self.chrono_animation_record = 0

        # Style des textes
        style = "Comic Sans MS"
        self.police_geante = pygame.font.SysFont(style, int(self.hauteur * 0.4), bold=True)
        self.police_mot = pygame.font.SysFont(style, int(self.hauteur * 0.25), bold=True)
        self.police_petite = pygame.font.SysFont("Arial", int(self.hauteur * 0.06), bold=True)
        self.police_message = pygame.font.SysFont(style, int(self.hauteur * 0.15), bold=True)

        self.demarrer_musique_et_sons()
        # le micro en mode moniteur
        threading.Thread(target=self.ecouter_le_micro, daemon=True).start()

    def demarrer_musique_et_sons(self):
        # Musique de fond
        if os.path.exists("assets/musique/ambiance.mp3"):
            pygame.mixer.music.load("assets/musique/ambiance.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)

        # son des lettres vol.2
        if os.path.exists("assets/sons/clic.mp3"):
            self.son_lettre = pygame.mixer.Sound("assets/sons/clic.mp3")
            self.son_lettre.set_volume(0.6)
        else:
            self.son_lettre = None

        # confettis (sons)
        if os.path.exists("assets/sons/confetti.mp3"):
            self.son_victoire = pygame.mixer.Sound("assets/sons/confetti.mp3")
        else:
            self.son_victoire = None

    def lire_le_record(self, chemin):
        if os.path.exists(chemin):
            try:
                with open(chemin, "r") as f:
                    return float(f.read())
            except:
                return 99.9
        return 99.9

    def choisir_nouvelle_touche(self):
        toutes_les_lettres = list(DICTIONNAIRE.keys())
        # yen auras pu deux lettre une apres l'autre
        nouvelle = random.choice(toutes_les_lettres)
        while nouvelle == self.derniere_touche:
            nouvelle = random.choice(toutes_les_lettres)

        self.touche_a_trouver = nouvelle
        self.derniere_touche = nouvelle

        if self.numero_module == 2:
            self.mot_actuel = DICTIONNAIRE[self.touche_a_trouver].upper()
            self.lettres_deja_tapees = ""

        self.moment_du_depart = time.time()

    def ecouter_le_micro(self):
        reconnaissance = sr.Recognizer()
        with sr.Microphone() as source_micro:
            reconnaissance.adjust_for_ambient_noise(source_micro, duration=1)
            while True:
                try:
                    son_micro = reconnaissance.listen(source_micro, phrase_time_limit=3)
                    phrase = reconnaissance.recognize_google(son_micro, language="fr-FR").lower()
                    if "merci" in phrase: self.ouvrir_video()
                    if "bye" in phrase: self.fermer_video()
                except:
                    pass

    def ouvrir_video(self):
        if os.path.exists(self.fichier_video):
            pygame.mixer.music.pause()
            subprocess.Popen(["xdg-open", self.fichier_video])
            self.message_bravo = "SURPRISE !";
            self.chrono_message = 120

    def fermer_video(self):
        os.system("pkill -f mpv || pkill -f vlc || pkill -f totem")
        self.message_bravo = "RETOUR AU JEU";
        self.chrono_message = 60
        pygame.mixer.music.unpause()

    def dessiner_les_infos(self):
        maintenant = time.time()
        temps_ecoule = maintenant - self.moment_du_depart if self.chrono_message <= 0 else 0
        texte_chrono = self.police_petite.render(f"{temps_ecoule:.1f}s", True, COULEURS["texte_fonce"])
        self.fenetre.blit(texte_chrono, (50, 40))

        record_actuel = self.record_module1 if self.numero_module == 1 else self.record_module2
        couleur_rec = COULEURS["violet_clair"]
        grossir = 1.0

        if self.numero_module == 1 and self.chrono_animation_record > 0:
            self.chrono_animation_record -= 1
            couleur_rec = COULEURS["jaune_etoile"]
            grossir = 1.2 + 0.1 * math.sin(self.chrono_animation_record * 0.3)

        police_rec = pygame.font.SysFont("Arial", int(self.hauteur * 0.05 * grossir), bold=True)
        txt_rec = police_rec.render(f"RECORD: {record_actuel:.1f}s", True, couleur_rec)
        self.fenetre.blit(txt_rec, (self.largeur - txt_rec.get_width() - 50, 40))

    def dessiner_menu(self):
        self.fenetre.fill(COULEURS["fond"])
        titre = self.police_message.render("ELIAS MAGIQUE", True, COULEURS["texte_fonce"])
        self.fenetre.blit(titre, titre.get_rect(center=(self.largeur // 2, self.hauteur * 0.25)))

        for i, (nom, desc, touche) in enumerate(
                [("MODULE 1", "Lettres Rapides", "1"), ("MODULE 2", "Mots Magiques", "2")]):
            cote = self.largeur * (0.3 if i == 0 else 0.7)
            boite = pygame.Rect(0, 0, self.largeur * 0.35, self.hauteur * 0.35)
            boite.center = (cote, self.hauteur * 0.6)
            pygame.draw.rect(self.fenetre, COULEURS["gris_lettre"], boite, border_radius=20)
            pygame.draw.rect(self.fenetre, COULEURS["violet_clair"], boite, 4, border_radius=20)

            s1 = self.police_petite.render(nom, True, COULEURS["texte_fonce"])
            s2 = self.police_petite.render(desc, True, COULEURS["violet_clair"])
            s3 = self.police_petite.render(f"Touche [{touche}]", True, COULEURS["rose"])
            self.fenetre.blit(s1, s1.get_rect(center=(boite.centerx, boite.centery - 50)))
            self.fenetre.blit(s2, s2.get_rect(center=(boite.centerx, boite.centery + 10)))
            self.fenetre.blit(s3, s3.get_rect(center=(boite.centerx, boite.centery + 70)))

    def quand_elias_reussit(self):
        temps_final = round(time.time() - self.moment_du_depart, 1)
        if self.numero_module == 1:
            if temps_final < self.record_module1:
                self.record_module1 = temps_final
                with open(self.fichier_record_m1, "w") as f: f.write(str(self.record_module1))
                self.chrono_animation_record = 90
        else:
            if temps_final < self.record_module2:
                self.record_module2 = temps_final
                with open(self.fichier_record_m2, "w") as f: f.write(str(self.record_module2))
                self.message_bravo = "NOUVEAU RECORD !";
                self.chrono_message = 80

        if self.son_victoire: self.son_victoire.play()
        for _ in range(50):
            self.liste_particules.append(Particule(self.largeur // 2, self.hauteur // 2, random.choice(
                [COULEURS["rose"], COULEURS["vert_succes"], COULEURS["jaune_etoile"]])))
        self.choisir_nouvelle_touche()

    def lancer_le_jeu(self):
        while True:
            if self.endroit_du_jeu == "MENU":
                self.dessiner_menu()
            else:
                self.fenetre.fill(COULEURS["fond"])
                self.dessiner_les_infos()
                if self.chrono_message > 0:
                    self.chrono_message -= 1
                    msg = self.police_message.render(self.message_bravo, True, COULEURS["rose"])
                    self.fenetre.blit(msg, msg.get_rect(center=(self.largeur // 2, self.hauteur // 2)))
                else:
                    if self.numero_module == 1:
                        img = self.police_geante.render(self.touche_a_trouver.upper(), True, COULEURS["texte_fonce"])
                        self.fenetre.blit(img, img.get_rect(center=(self.largeur // 2, self.hauteur // 2)))
                    else:
                        fond_m = self.police_mot.render(self.mot_actuel, True, COULEURS["gris_lettre"])
                        rect_m = fond_m.get_rect(center=(self.largeur // 2, self.hauteur // 2))
                        self.fenetre.blit(fond_m, rect_m)
                        tape_m = self.police_mot.render(self.lettres_deja_tapees, True, COULEURS["vert_succes"])
                        self.fenetre.blit(tape_m, rect_m)

            for p in self.liste_particules[:]:
                p.bouger()
                if p.vie <= 0:
                    self.liste_particules.remove(p)
                else:
                    pygame.draw.circle(self.fenetre, p.couleur, (int(p.x), int(p.y)), int(p.taille * p.vie))

            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT: pygame.quit(); sys.exit()

                if evenement.type == pygame.KEYDOWN:
                    if evenement.key == pygame.K_ESCAPE:
                        if self.endroit_du_jeu == "JOUER":
                            self.endroit_du_jeu = "MENU"
                        else:
                            pygame.quit(); sys.exit()

                    if self.endroit_du_jeu == "MENU":
                        if evenement.key in [pygame.K_1, pygame.K_KP1]:
                            self.numero_module = 1;
                            self.endroit_du_jeu = "JOUER";
                            self.choisir_nouvelle_touche()
                        elif evenement.key in [pygame.K_2, pygame.K_KP2]:
                            self.numero_module = 2;
                            self.endroit_du_jeu = "JOUER";
                            self.choisir_nouvelle_touche()

                    elif self.endroit_du_jeu == "JOUER" and self.chrono_message <= 0:
                        lettre = evenement.unicode.upper()
                        if self.numero_module == 1:
                            if lettre.lower() == self.touche_a_trouver: self.quand_elias_reussit()
                        else:
                            if len(self.lettres_deja_tapees) < len(self.mot_actuel):
                                if lettre == self.mot_actuel[len(self.lettres_deja_tapees)]:
                                    self.lettres_deja_tapees += lettre
                                    # debug du son vol.2
                                    if self.son_lettre: self.son_lettre.play()
                                    if self.lettres_deja_tapees == self.mot_actuel: self.quand_elias_reussit()

            pygame.display.flip()
            self.horloge.tick(60)


if __name__ == "__main__":
    JeuElias().lancer_le_jeu()
