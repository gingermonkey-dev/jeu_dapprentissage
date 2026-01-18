import os
from PIL import Image, ImageDraw, ImageFont

# --- CONFIGURATION ---
OUTPUT_DIR = "assets/images"
CANVAS_SIZE = (800, 800)  # Taille de l'image carrée
FONT_SIZE = 750  # Taille de la lettre (presque aussi grande que le canvas)

# Couleurs pour les lettres (Elias va adorer le contraste)TTRE = (80, 150, 250)  # Bleu
COULEUR_CHIFFRE = (255, 120, 0)  # Orange
FONT_PATH = "/usr/share/fonts/google-noto/NotoSans-Bold.ttf"  # Chemin Fedora standard


def generate_image(text, filename, color):
    img = Image.new('RGBA', CANVAS_SIZE, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except:
        font = ImageFont.load_default()
        print("Attention: Police Noto non trouvée, utilisation de la police par défaut.")

    # centrer
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (CANVAS_SIZE[0] - w) / 2 - bbox[0]
    y = (CANVAS_SIZE[1] - h) / 2 - bbox[1]

    draw.text((x, y), text, fill=color, font=font)

    # Sauvegarde
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    img.save(os.path.join(OUTPUT_DIR, f"{filename}.png"))
    print(f"Généré : {filename}.png")


def main():
    # Générer Alphabet
    for i in range(26):
        lettre = chr(65 + i).lower()
        generate_image(lettre.upper(), f"lettre_{lettre}", COULEUR_LETTRE)

    # Générer Chiffres
    for i in range(10):
        generate_image(str(i), f"chiffre_{i}", COULEUR_CHIFFRE)


if __name__ == "__main__":
    main()