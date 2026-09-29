# -*- coding: utf-8 -*-
"""Notes presse relevées en septembre 2026, converties sur 10.
Clé = identifiant du PC dans le catalogue de l'artefact.
- 'notes' : liste (média, note sur 10)
- 'agg'   : (moyenne sur 10, nombre de notes) quand seule la moyenne d'un agrégateur est disponible
- 'scope' : 'modele' (ce modèle précis) ou 'gamme' (même gamme / génération, autre configuration)
- 'src'   : (libellé, url) de la source principale
Absence de clé = pas encore de test presse noté trouvé."""

def p(v): return v / 10          # x/100 -> /10
def s5(v): return v * 2          # x/5 -> /10

NBC = "Notebookcheck"

PRESS = {
    # ---------- Bureautique ----------
    "zenbook-a14-ux3407qa": dict(scope="modele", src=("Synthèse Notebookcheck", "https://www.notebookcheck.com/Asus-ZenBook-A14-Serie.1062545.0.html"),
        notes=[(NBC, p(86.3)), ("PC Welt", 7), ("TechRadar", 8), ("CNET", 8.5), ("PCWorld", 7.8), ("T3", 8), ("Trusted Reviews", 8),
               ("Creative Bloq", 8), ("Expert Reviews", 8), ("Stuff", 8), ("India Today", 7.5), ("Geek Culture", 7.7), ("NDTV Gadgets", 8),
               ("91mobiles", 7.5), ("Gadgetguy", 8.6), ("Engadget", 7.8), ("Tom's Guide", 7), ("MobileSyrup", 9), ("IT Pro", 8),
               ("Ultrabook Review", 8), ("TechPP", 8.2)]),
    "surface-pro-12-copilot": dict(scope="modele", src=("Synthèse CommentChoisir", "https://www.commentchoisir.fr/en/review-Microsoft_Surface+Pro+12.htm"),
        notes=[("IT Pro", s5(5)), (NBC, p(86)), ("Expert Reviews", s5(4)), ("Frandroid", 7), ("TechRadar", s5(3)), ("Trusted Reviews", s5(3)),
               ("Journal du Geek", 6), ("Presse-Citron", 6), ("Les Numériques", s5(2))]),
    "ideapad-slim3-15q8x10": dict(scope="modele", src=("Test Labo Fnac", "https://leclaireur.fnac.com/test/677593-test-labo-du-lenovo-ideapad-slim-3-gen10-un-laptop-ambitieux-qui-rate-la-marche/"),
        notes=[("Labo Fnac", s5(3))]),
    "galaxy-book4-edge-156": dict(scope="modele", src=("Test Notebookcheck", "https://www.notebookcheck.net/Snapdragon-and-18-hours-of-battery-life-for-700-Samsung-Galaxy-Book4-Edge-15-Copilot-review.1141585.0.html"),
        notes=[(NBC, p(82))]),
    "aspire-go15-ag15-42p-r99j-neuf": dict(scope="gamme", src=("Synthèse CommentChoisir (gamme Aspire Go 15)", "https://www.commentchoisir.fr/en/review-Acer_Aspire+Go+15.htm"),
        agg=(s5(3.7), 6)),
    # ---------- Création ----------
    "macbook-pro14-m5": dict(scope="modele", src=("Test Notebookcheck", "https://www.notebookcheck.com/Test-Apple-MacBook-Pro-M5-2025-Der-schnellste-Single-Core-Prozessor-der-Welt.1142597.0.html"),
        notes=[(NBC, p(91))]),
    "proart-p16-h7606wm": dict(scope="gamme", src=("Test Notebookcheck (ProArt P16 2025, RTX 5070)", "https://www.notebookcheck.net/4K-OLED-is-replaced-by-120-Hz-2-8K-OLED-Asus-ProArt-P16-with-RTX-5070-Laptop-review.1026301.0.html"),
        notes=[(NBC, p(89))]),
    "yoga-pro7-15iph11": dict(scope="modele", src=("Synthèse Notebookcheck", "https://www.notebookcheck.net/Lenovo-Yoga-Pro-7-15IPH11.1309251.0.html"),
        notes=[(NBC, p(90.4)), ("Times of India", 8.5), ("T3", 8), ("Tom's Guide", 8), ("MakeUseOf", 6)]),
    # ---------- Gaming ----------
    "omen-max-16-ak0002nf": dict(scope="modele", src=("Synthèse CommentChoisir", "https://www.commentchoisir.fr/test-HP_Omen+Max+16.htm"),
        notes=[("RTINGS", 9), (NBC, p(82)), ("Windows Central", 8), ("Clubic", 8), ("GamesRadar", s5(4)), ("Phonandroid", s5(4)),
               ("T3", s5(4)), ("TechRadar", s5(4)), ("Mac Sources", 8), ("KitGuru", 7), ("Tom's Hardware", s5(3)), ("PCWorld", s5(3))]),
    "predator-helios-neo16": dict(scope="modele", src=("Synthèse Notebookcheck", "https://www.notebookcheck.net/Acer-Predator-Helios-Neo-16-AI-PHN16-73.1171432.0.html"),
        notes=[("ITC.ua", p(76))]),
    "msi-vector16-a2xwig-5080": dict(scope="gamme", src=("Test Notebookcheck (Vector 16 HX AI, RTX 5070 Ti)", "https://www.notebookcheck.com/MSI-Vector-16-HX-AI-im-Test-Opulenter-Gaming-Laptop-mit-RTX-5070-Ti.1034000.0.html"),
        notes=[(NBC, p(84))]),
    "legion5-15ahp11": dict(scope="gamme", src=("Test Notebookcheck (Legion 5 Gen 11, RTX 5060)", "https://www.notebookcheck.net/OLED-AMD-gamer-with-32-GB-RAM-Lenovo-Legion-5-15AGP11-laptop-review.1333407.0.html"),
        notes=[(NBC, p(85))]),
    "rog-strix-g18": dict(scope="gamme", src=("Synthèse Notebookcheck (Strix G18 2025)", "https://www.notebookcheck.com/Asus-ROG-Strix-G18-2025-Serie.1079465.0.html"),
        notes=[(NBC + " (G815LW)", p(87)), (NBC + " (G815LP)", p(90)), ("PCMag", 7), ("Android Authority", 10), ("XDA Developers", 7.5),
               ("Laptop Mag", 9), ("Game IT", 10), ("Computerhoy", 9.5), ("Profesional Review", 9), ("MuyComputer", 8.5)]),
    "nitro-v16-anv16-42": dict(scope="modele", src=("Synthèse Notebookcheck", "https://www.notebookcheck.com/Acer-Nitro-V-16-Serie.1178239.0.html"),
        notes=[(NBC, p(77.5)), ("PC Welt", 7.8), ("Tom's Guide", 7), ("PCMag", 8), ("PCWorld", 7), ("Charles Tech", 7.8)]),
    "msi-crosshair16-d2xwgkg": dict(scope="modele", src=("Synthèse Notebookcheck", "https://www.notebookcheck.com/MSI-Crosshair-16-Serie.1078133.0.html"),
        notes=[(NBC, p(82.2)), ("PC Gamer", 7.5), ("Clubic", 8), ("T3 (Pologne)", 4.3)]),
    "loq-15irx10": dict(scope="modele", src=("Synthèse Notebookcheck", "https://www.notebookcheck-cn.com/Lenovo-LOQ-15IRX10.1096033.0.html"),
        notes=[("Chip.de", 8.8), ("Zive", 8)]),
    # ---------- Polyvalent ----------
    "lg-gram-14z90r": dict(scope="gamme", src=("Synthèse CommentChoisir (gamme Gram 14)", "https://www.commentchoisir.fr/test-LG_Gram+14.htm"),
        agg=(s5(3.9), 25)),
    "surface-laptop7-13": dict(scope="modele", src=("Synthèse Notebookcheck", "https://www.notebookcheck.com/Microsoft-Surface-Laptop-7-Serie.913071.0.html"),
        notes=[(NBC, p(86.9)), ("TechRadar", 10), ("Engadget", 8.8), ("The Verge", 8), ("Trusted Reviews", 9)]),
    "yoga-slim7-ultra-14iph11": dict(scope="modele", src=("Test Notebookcheck", "https://www.notebookcheck.net/Lenovo-Yoga-Slim-7-Ultra-14IPH11-review-Best-XPS-14-alternative-yet.1280307.0.html"),
        notes=[(NBC, p(85))]),
    "ideapad-slim5-14q8x9": dict(scope="modele", src=("Synthèse Notebookcheck", "https://www.notebookcheck.net/Lenovo-IdeaPad-Slim-5-14Q8X9.938501.0.html"),
        notes=[("XDA Developers", 8), ("Les Numériques", 6)]),
    "yoga-slim7-14akp10": dict(scope="modele", src=("Test Notebookcheck", "https://www.notebookcheck.net/Brilliant-1-100-nit-OLED-but-unexpected-quality-issues-Lenovo-Yoga-Slim-7-14-G10-review.1017693.0.html"),
        notes=[(NBC, p(85))]),
    "vivobook16-m1605naq": dict(scope="gamme", src=("Synthèse Notebookcheck (Vivobook 16 M1605)", "https://www.notebookcheck.net/Asus-Vivobook-16-M1605YA.779619.0.html"),
        notes=[("Pokde", 8.3), ("Hitech Century", 7.4), ("Computerbild", 8.9)]),
}

# Gammes partagées par plusieurs références
AERO = dict(scope="gamme", src=("Synthèse Notebookcheck + CommentChoisir (gamme Aero X16 2025)", "https://www.notebookcheck.com/Gigabyte-Aero-X16-Serie.1090594.0.html"),
    notes=[(NBC, p(83.7)), ("PC Gamer", 6.9), ("Profesional Review", 9), ("Multiplayer.it", 7.5), ("Les Numériques", 6), ("HardwareZone", 8.5),
           ("MuyComputer (1VH)", 8.8), ("Geeknetic", 9), ("Smart World", 8), ("MuyComputer (2WHA)", 9), ("Tweakers", 10), ("Frandroid", 8),
           ("TechPowerUp", 10), ("Tom's Hardware", 6), ("Chip.de", 6)])
for k in ["aero-x16-1wh93", "aero-x16-2wha3", "aero-x16-1vh93", "aero-x16-3vhl3"]:
    PRESS[k] = AERO

A16 = dict(scope="gamme", src=("Synthèse Notebookcheck (gamme Gaming A16 2025)", "https://www.notebookcheck.com/Gigabyte-Gaming-A16-Serie.1076872.0.html"),
    notes=[(NBC, p(80.1)), ("MuyComputer", 8.9), ("Profesional Review", 8.3), ("PC Gamer", 7.3), ("Mezha", 8), ("Clubic", 8), ("Gadgetguy", 7.7)])
for k in ["gigabyte-a16-3whk3", "gigabyte-a16-3thk3"]:
    PRESS[k] = A16

GO15 = PRESS["aspire-go15-ag15-42p-r99j-neuf"]
for k in ["aspire-go15-recond", "aspire-go15-ryzen3"]:
    PRESS[k] = GO15
