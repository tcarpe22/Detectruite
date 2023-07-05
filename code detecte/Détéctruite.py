###IMPORTATIONS DES PACKAGES
import os
import cv2
import time
import math
import numpy as np
import pandas as pd
import tkinter as tk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from tkinter import ttk, filedialog
########

#Création d'une variable redirigeant vers le répertoire
repertoire = os.path.dirname(os.path.abspath(__file__))
repertoire = os.path.normpath(repertoire)

path = ""
video_choice = ""

#Fonction d'ouverture 
def open_video(file):
    global path
    path = file
    window1.destroy() #Fermeture de la fenêtre

#Fonction de gestion du bouton n°1
def on_button1_click():
    global path
    #Boîte de dialogue avec l'utilisateur permettant d'importer uniquement des fichiers au format mp4 ou avi
    path = filedialog.askopenfilename(filetypes=[("Fichiers vidéo", "*.mp4;*.avi")])
    open_video(path) #Ouverture du chemin de la vidéo

#Fonction de gestion du bouton n°2
def on_button2_click():
    exec(open(f'{repertoire}/Pick_Color.py').read())

#Création des fenêtres
window1 = tk.Tk()
window2 = None

#Ajoute la fenêtre à la liste
windows = [window1]

#Chargement de l'image pour le background (style)
image = Image.open(f"{repertoire}/image/truite.png")
image = image.resize((1024, 1024), Image.ANTIALIAS)
background_image = ImageTk.PhotoImage(image)

#Widget pour afficher l'image en background
background_label = tk.Label(window1, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

window1.geometry("1024x720") #Taille de fenêtre largeurxlongueur

#Obtention des dimensions d'écran
screen_width = window1.winfo_screenwidth()
screen_height = window1.winfo_screenheight()

#Calcul des coordonnées pour centrer la fenêtre
x = int(screen_width / 2 - 1024 / 2)
y = int(screen_height / 2 - 720 / 2)

#Positionner au centre de l'écran
window1.geometry(f"1024x720+{x}+{y}")

#Utiliser le style par défaut pour les boutons
style = ttk.Style()
style.theme_use("alt")

#Style des boutons
style.configure("TButton",
                font=("Arial", 12),  # Police du texte
                width=10,  # Largeur du bouton
                foreground="black",  # Couleur du texte
                background="#00ffff",  # Couleur de fond
                padding=10,  # Espacement interne
                )

#Cadre pour contenir les boutons
frame = ttk.Frame(window1)

#Chargement de l'image pour le background (style)
background_but = Image.open(f"{repertoire}/image/R.jpg")
background_but = background_but.resize((360, 150), Image.ANTIALIAS)
background_button = ImageTk.PhotoImage(background_but)

#Widget pour afficher l'image en background
background_label = ttk.Label(frame, image=background_button)
background_label.place(x=0, y=0, relwidth=1, relheight=1.5, anchor="nw", rely=-0.35)

#Titre
title_label = ttk.Label(frame, text="Détéctruite", font=("Arial", 16))
title_label.grid(row=0, column=0, columnspan=3, pady=(50, 10))

#Création des boutons
button1 = ttk.Button(frame, text="Vidéo", command=on_button1_click)
button2 = ttk.Button(frame, text="Testeur", command=on_button2_click)

#Centrer les boutons horizontalement
button1.grid(row=1, column=0, padx=10)
button2.grid(row=1, column=1, padx=10)

#Centrer le cadre dans la fenêtre
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

#Changer le titre de la fenêtre
window1.title("Détéctruite")
window1.iconbitmap(f"{repertoire}/image/truite.ico")

#Boucle principale de la fenêtre
window1.mainloop()

if path == "":
    exit()

print("Chemin de la vidéo sélectionnée :", path)

#Capture de la vidéo
cap = cv2.VideoCapture(path)

###Initialisation des plages de couleurs en HSV###
lower_range_blue = np.array([107, 113, 121])
upper_range_blue = np.array([114, 179, 198])

lower_range_green = np.array([46, 101, 88])
upper_range_green = np.array([99, 206, 118])

lower_range_yellow = np.array([0, 121, 116])
upper_range_yellow = np.array([44, 255, 255])

lower_fish = np.array([0, 0, 0])
upper_fish = np.array([179, 255, 76])
#####

#Détection et traitement du bleu
def blue(img):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image, lower_fish, upper_fish)
    image = cv2.blur(image, (7, 7))
    mask = cv2.erode(mask, None, iterations=4)
    mask = cv2.dilate(mask, None, iterations=4)
    image2 = cv2.bitwise_and(frame, frame, mask=mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mask2 = cv2.inRange(image, lower_range_blue, upper_range_blue)
    contours2, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Trouver le contour externe du bac
    if len(contours2) > 0:
        bac_contour = max(contours2, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(bac_contour)
        x_min = x
        x_max = x + w
        y_min = y
        y_max = y + h
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

    #Réinitialisation des poissons détectés à chaque itération
    fish_positions2 = []

    for contour in contours:
        ((x, y), rayon) = cv2.minEnclosingCircle(contour)
        if rayon > 50 and x > x_min and x < x_max and y > y_min and y < y_max:
            fish_positions2.append((x, y))

    #Limiter le nombre de poissons détectés au nombre spécifié
    fish_positions2 = fish_positions2[:1]

    for position in fish_positions2:
        x, y = position
        cv2.circle(image2, (int(x), int(y)), 5, (255, 255, 0), 10)
        cv2.putText(frame, f"Poisson", (int(x) + 10, int(y) - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 0), 1, cv2.LINE_AA)
        cv2.circle(frame, (int(x), int(y)), 5, (255, 255, 0), 10)
        cv2.line(frame, (int(x), int(y)), (int(x) + 150, int(y)), (255, 255, 0), 2)

        if prev_positions:
            prev_x, prev_y = prev_positions.pop(0)
            distance_pixels = np.sqrt((x - prev_x) ** 2 + (y - prev_y) ** 2)
            elapsed_time = time.time() - start_time

            fish_speed = distance_pixels / elapsed_time
            fish_speeds.append(fish_speed)


        prev_positions.append(position)
        cv2.imshow('Poisson', image2)
        #cv2.imshow('Bac bleu', mask2)
    
#Détection et traitement du vert
def green(img):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image, lower_fish, upper_fish)
    image = cv2.blur(image, (7, 7))
    mask = cv2.erode(mask, None, iterations=4)
    mask = cv2.dilate(mask, None, iterations=4)
    image2 = cv2.bitwise_and(frame, frame, mask=mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mask2 = cv2.inRange(image, lower_range_green, upper_range_green)
    contours2, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Trouver le contour externe du bac
    if len(contours2) > 0:
        bac_contour = max(contours2, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(bac_contour)
        x_min = x
        x_max = x + w
        y_min = y
        y_max = y + h
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #Réinitialisation des poissons détectés à chaque itération
    fish_positions2 = []

    for contour in contours:
        ((x, y), rayon) = cv2.minEnclosingCircle(contour)
        if rayon > 50 and x > x_min and x < x_max and y > y_min and y < y_max:
            fish_positions2.append((x, y))

    #Limiter le nombre de poissons détectés au nombre spécifié
    fish_positions2 = fish_positions2[:1]

    for position in fish_positions2:
        x, y = position
        cv2.circle(image2, (int(x), int(y)), 5, (0, 255, 0), 10)
        cv2.putText(frame, f"Poisson", (int(x) + 10, int(y) - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), 10)
        cv2.line(frame, (int(x), int(y)), (int(x) + 150, int(y)), (0, 255, 0), 2)

        if prev_positions2:
            prev_x, prev_y = prev_positions2.pop(0)
            distance_pixels = np.sqrt((x - prev_x) ** 2 + (y - prev_y) ** 2)
            elapsed_time = time.time() - start_time

            fish_speed = distance_pixels / elapsed_time
            fish_speeds2.append(fish_speed)


        prev_positions2.append(position)
        cv2.imshow('Poisson', image2)
        #cv2.imshow('Bac Vert', mask2)

#Détection et traitement du jaune
def yellow(img):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image, lower_fish, upper_fish)
    image = cv2.blur(image, (7, 7))
    mask = cv2.erode(mask, None, iterations=4)
    mask = cv2.dilate(mask, None, iterations=4)
    image2 = cv2.bitwise_and(frame, frame, mask=mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mask2 = cv2.inRange(image, lower_range_yellow, upper_range_yellow)
    contours2, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Trouver le contour externe du bac
    if len(contours2) > 0:
        bac_contour = max(contours2, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(bac_contour)
        x_min = x
        x_max = x + w
        y_min = y
        y_max = y + h
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

    #Réinitialisation des poissons détectés à chaque itération
    fish_positions3 = []

    for contour in contours:
        ((x, y), rayon) = cv2.minEnclosingCircle(contour)
        if rayon > 50 and x > x_min and x < x_max and y > y_min and y < y_max:
            fish_positions3.append((x, y))

    #Limiter le nombre de poissons détectés au nombre spécifié
    fish_positions3 = fish_positions3[:1]

    for position in fish_positions3:
        x, y = position
        cv2.circle(image2, (int(x), int(y)), 5, (0, 255, 255), 10)
        cv2.putText(frame, f"Poisson", (int(x) + 10, int(y) - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 255), 10)
        cv2.line(frame, (int(x), int(y)), (int(x) + 150, int(y)), (0, 255, 255), 2)

        if prev_positions3:
            prev_x, prev_y = prev_positions3.pop(0)
            distance_pixels = np.sqrt((x - prev_x) ** 2 + (y - prev_y) ** 2)
            elapsed_time = time.time() - start_time

            fish_speed = distance_pixels / elapsed_time
            fish_speeds3.append(fish_speed)


        prev_positions3.append(position)
        cv2.imshow('Poisson', image2)
        #cv2.imshow('Bac jaune', mask2)

#Listes pour stocker les vitesses des poissons de chaque bac
fish_speeds = []
fish_speeds2 = []
fish_speeds3 = []

#Listes pour stocker les positions précédentes des poissons de chaque bac
prev_positions = []
prev_positions2 = []
prev_positions3 = []

#Récupérer la durée de la vidéo
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration_video = frame_count / fps

#Début du chrono
start_time = time.time()

#Boucle infinie
while True:
    
    ret, frame = cap.read()
    if not ret:
        break #Sortie de boucle si la vidéo ne peut pas être lue
    
    green(frame)
    yellow(frame)
    blue(frame)

    #Temps écoulé
    elapsed_time = time.time() - start_time

    #Arrondir elapsed_time à l'entier supérieur
    elapsed_time = math.ceil(elapsed_time)

    #Chronomètre
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)

    #Vérifier si le chronomètre a atteint la durée de la vidéo
    if elapsed_time >= duration_video:
        break

    #Affichage du chrono sous la forme HH:MM:SS
    cv2.putText(frame, "{:02}:{:02}:{:02}".format(hours, minutes, seconds), (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (0, 0, 255), 2)

    #Affichage de la fenêtre de vidéo
    cv2.imshow("Parcours du poisson", frame)

    #Attend une touche clavier
    key = cv2.waitKey(1)

    if key == 27:  # 27 = touche Echap
        break

cap.release() #Libérer les ressources
cv2.destroyAllWindows() #Fermeture des fenêtres

#Fonction de temps pour les graphiques en sortie
def time():
    plt.axvspan(0, 300, facecolor='green', alpha=0.3)
    plt.axvspan(300, 600, facecolor='black', alpha=0.3)
    plt.axvspan(600, 900, facecolor='orange', alpha=0.3)
    plt.axvspan(900, 1500, facecolor='black', alpha=0.3)

###AFFICHAGE DES GRAPHIQUES###
fig = plt.figure(figsize=(15, 6))
ax1 = fig.add_subplot(321) #Affichage en 3 lignes, 2 colonnes, position 1
ax2 = fig.add_subplot(323) #Affichage en 3 lignes, 2 colonnes, position 3
ax3 = fig.add_subplot(325) #Affichage en 3 lignes, 2 colonnes, position 5

plt.subplot(3, 2, 1)
plt.plot(fish_speeds)
plt.xlabel("Temps (min)") #Abscisses
plt.ylabel("Vitesse (m/s)") #Ordonnées
plt.title("Graphique des vitesses Bac Bleu") #Titre
plt.grid(True, color="grey") #Quadrillage
ax1.plot(fish_speeds, color='#00FFFF') #Couleur du graphique associée à celle du bac
#Temps d'acclimatation et de perturbation
time()

#Définir les limites de l'axe des x
plt.xlim(0, elapsed_time)

plt.subplot(3, 2, 3)
plt.plot(fish_speeds2)
plt.xlabel("Temps (min)") #Abscisses
plt.ylabel("Vitesse (m/s)") #Ordonnées
plt.title("Graphique des vitesses Bac Vert") #Titre
plt.grid(True, color="grey") #Quadrillage
ax2.plot(fish_speeds2, color='#00FF00') #Couleur du graphique associée à celle du bac
#Temps d'acclimatation et de perturbation
time()

#Définir les limites de l'axe des x
plt.xlim(0, elapsed_time)

plt.subplot(3, 2, 5)
plt.plot(fish_speeds3)
plt.xlabel("Temps (min)") #Abscisses
plt.ylabel("Vitesse (m/s)") #Ordonnées
plt.title("Graphique des vitesses Bac Jaune") #Titre
plt.grid(True, color="grey") #Quadrillage
ax3.plot(fish_speeds3, color='#FFFF00') #Couleur du graphique associée à celle du bac
#Temps d'acclimatation et de perturbation
time()

#Définir les limites de l'axe des x
plt.xlim(0, elapsed_time)
#####

###AFFICHAGE DES DIAGRAMMES CIRCULAIRES###
#Initialisation des vitesses max
v_max_blue = max(fish_speeds)
v_max_green = max(fish_speeds2)
v_max_yellow = max(fish_speeds3)

#Liste pour les types de stress
stress_types1 = []

#BLEU#
#Calcul du pourcentage de stress bleu
stress_fort1 = len([v for v in fish_speeds if v >= 0.6 * v_max_blue]) #Supérieur ou égale à 60% de vitesse max
stress_moyen1 = len([v for v in fish_speeds if 0.4 * v_max_blue <= v < 0.6 * v_max_blue]) #Compris entre 40% et 60% strictement
stress_faible1 = len([v for v in fish_speeds if 0.2 * v_max_blue <= v < 0.4 * v_max_blue]) #Compris entre 20% et 40% strictement
calme1 = len([v for v in fish_speeds if 0.05 * v_max_blue < v < 0.2 * v_max_blue]) #Compris entre 5% strictement et 20% strictement
immobile1 = len([v for v in fish_speeds if v <= 0.05 * v_max_blue]) #Inférieur ou égale à 5%

#Parcourt les valeurs de fish_speeds et détermine le type de stress correspondant
for v in fish_speeds:
    if v >= 0.6 * v_max_blue:
        stress_types1.append('Stress fort')
    elif 0.4 * v_max_blue <= v < 0.6 * v_max_blue:
        stress_types1.append('Stress moyen')
    elif 0.2 * v_max_blue <= v < 0.4 * v_max_blue:
        stress_types1.append('Stress faible')
    elif 0.05 * v_max_blue < v < 0.2 * v_max_blue:
        stress_types1.append('Calme')
    else:
        stress_types1.append('Immobile')

sizes1 = [stress_fort1, stress_moyen1, stress_faible1, calme1, immobile1]
colors = ['#FF0000', '#FFA500', '#FFFF00', '#00FF00', '#C0C0C0']  #Couleurs pour les portions du diagramme circulaire

#Filtrer les segments avec 0% pour bleu
filtered_sizes1 = [size for size in sizes1 if size != 0]
filtered_colors1 = [color for size, color in zip(sizes1, colors) if size != 0]

#Création du diagramme circulaire bac bleu
plt.subplot(3, 2, 2)
plt.pie(filtered_sizes1, colors=filtered_colors1, autopct='%1.1f%%', startangle=90, radius=1.2, wedgeprops=dict(edgecolor='black', linewidth=0.7))
plt.title('Niveau de stress du poisson Bac Bleu') #Titre

#VERT#
#Calcul du pourcentage de stress vert
stress_fort2 = len([v for v in fish_speeds2 if v >= 0.6 * v_max_green]) #Supérieur ou égale à 60% de vitesse max
stress_moyen2 = len([v for v in fish_speeds2 if 0.4 * v_max_green <= v < 0.6 * v_max_green]) #Compris entre 40% et 60% strictement
stress_faible2 = len([v for v in fish_speeds2 if 0.2 * v_max_green <= v < 0.4 * v_max_green]) #Compris entre 20% et 40% strictement
calme2 = len([v for v in fish_speeds2 if 0.05 * v_max_green < v < 0.2 * v_max_green]) #Compris entre 5% strictement et 20% strictement
immobile2 = len([v for v in fish_speeds2 if v <= 0.05 * v_max_green]) #Inférieur ou égale à 5%

sizes2 = [stress_fort2, stress_moyen2, stress_faible2, calme2, immobile2]

#Filtrer les segments avec 0% pour vert
filtered_sizes2 = [size for size in sizes2 if size != 0]
filtered_colors2 = [color for size, color in zip(sizes2, colors) if size != 0]

#Création du diagramme circulaire bac vert
plt.subplot(3, 2, 4)
plt.pie(filtered_sizes2, colors=filtered_colors2, autopct='%1.1f%%', startangle=90, radius=1.2, wedgeprops=dict(edgecolor='black', linewidth=0.7))
plt.title('Niveau de stress du poisson Bac Vert') #Titre

#Centrer la légende à côté des graphiques circulaires
plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)

#Ajout de la légende
legend_labels = ['Stress fort', 'Stress moyen', 'Stress faible', 'Calme', 'Immobile']
plt.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0.5))

#JAUNE#
#Calcul du pourcentage de stress jaune
stress_fort3 = len([v for v in fish_speeds3 if v >= 0.6 * v_max_yellow]) #Supérieur ou égale à 60% de vitesse max
stress_moyen3 = len([v for v in fish_speeds3 if 0.4 * v_max_yellow <= v < 0.6 * v_max_yellow]) #Compris entre 40% et 60% strictement
stress_faible3 = len([v for v in fish_speeds3 if 0.2 * v_max_yellow <= v < 0.4 * v_max_yellow]) #Compris entre 20% et 40% strictement
calme3 = len([v for v in fish_speeds3 if 0.05 * v_max_yellow < v < 0.2 * v_max_yellow]) #Compris entre 5% strictement et 20% strictement
immobile3 = len([v for v in fish_speeds3 if v <= 0.05 * v_max_yellow]) #Inférieur ou égale à 5%

sizes3 = [stress_fort3, stress_moyen3, stress_faible3, calme3, immobile3]

#Filtrer les segments avec 0% pour jaune
filtered_sizes3 = [size for size in sizes3 if size != 0]
filtered_colors3 = [color for size, color in zip(sizes3, colors) if size != 0]

#Création du diagramme circulaire bac jaune
plt.subplot(3, 2, 6)
plt.pie(filtered_sizes3, colors=filtered_colors3, autopct='%1.1f%%', startangle=90, radius=1.2, wedgeprops=dict(edgecolor='black', linewidth=0.7))
plt.title('Niveau de stress du poisson Bac Jaune') #Titre

#Définition du titre principal de la fenêtre
window_name = 'Diagrammes circulaires'
plt.suptitle(window_name, fontsize=16)

#Affichage
plt.show()

#####EXCEL#####
#Arrondir elapsed_time à l'entier supérieur
elapsed_time = math.ceil(elapsed_time)

#Définition de la variable de temps avec une séquence de temps
times = list(range(0, elapsed_time + 1, 1))  #Intervalles de 1 seconde

#Assurer que les tableaux de données ont la même longueur
length = min(len(times), len(fish_speeds), len(fish_speeds2), len(fish_speeds3))
times = times[:length]
fish_speeds = fish_speeds[:length]
fish_speeds2 = fish_speeds2[:length]
fish_speeds3 = fish_speeds3[:length]

#Arrondir les valeurs à 10^-3
fish_speeds = [round(speed, 3) for speed in fish_speeds]
fish_speeds2 = [round(speed, 3) for speed in fish_speeds2]
fish_speeds3 = [round(speed, 3) for speed in fish_speeds3]

interval_duration = 30  # Durée de l'intervalle en secondes

# Calcul des intervalles de temps
interval_times = list(range(0, elapsed_time + 1, interval_duration))

avg_speeds_blue = [sum(fish_speeds[max(0, i - interval_duration):i]) / min(i, interval_duration) if i != 0 else 0 for i in interval_times]
avg_speeds_green = [sum(fish_speeds2[max(0, i - interval_duration):i]) / min(i, interval_duration) if i != 0 else 0 for i in interval_times]
avg_speeds_yellow = [sum(fish_speeds3[max(0, i - interval_duration):i]) / min(i, interval_duration) if i != 0 else 0 for i in interval_times]


#Arrondir les valeurs à 10^-3
avg_speeds_blue = [round(speed, 3) for speed in avg_speeds_blue]
avg_speeds_green = [round(speed, 3) for speed in avg_speeds_green]
avg_speeds_yellow = [round(speed, 3) for speed in avg_speeds_yellow]

#Liste vide avec la même longueur que times pour exportation
empty = [""] * len(times)
empty2 = [""] * len(interval_times)

# Retiré la valeurs de 0 dans le tableau exel "vitesse moyenne"
interval_times = interval_times[1:]
empty2 = empty2[1:]
avg_speeds_blue = avg_speeds_blue[1:]
avg_speeds_green = avg_speeds_green[1:]
avg_speeds_yellow = avg_speeds_yellow[1:]

#Dictionnaires des données
data = {
    'Temps': times,  # Valeurs de temps
    '': empty,
    'Vitesse bleu (m/s)': fish_speeds,  # Vitesse du bac bleu
    'Vitesse vert (m/s)': fish_speeds2,  # Vitesse du bac vert
    'Vitesse jaune (m/s)': fish_speeds3,  # Vitesse du bac jaune
}

# Créer un dictionnaire des données
data2 = {
    'Temps': interval_times,  # Intervalle de temps (0, 30, 60, etc.)
    '': empty2,
    'Moyenne Vitesse Bac Bleu (m/s)': avg_speeds_blue,  # Vitesse moyenne des 30 dernières secondes
    'Moyenne Vitesse Bac Vert (m/s)': avg_speeds_green,
    'Moyenne Vitesse Bac Jaune (m/s)': avg_speeds_yellow
}

# Arrondir les valeurs à 10^-3
v_max_blue = round(v_max_blue, 3)
v_max_green = round(v_max_green, 3)
v_max_yellow = round(v_max_yellow, 3)

data3 = {
    'Vitesse Max Bac Bleu': v_max_blue,  # Vitesse max
    'Vitesse Max Bac Vert': v_max_green,
    'Vitesse Max Bac Jaune': v_max_yellow
}


#Création des dataframes
df = pd.DataFrame(data)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)

#Obtenir le chemin complet du bureau
bureau = os.path.join(os.path.expanduser("~"), "Desktop")

#Mettre le fichier Excel sur le bureau
chemin_fichier_excel = os.path.join(bureau, "Donnees_brutes.xlsx")
chemin_fichier_excel2 = os.path.join(bureau, "Vitesses_moyennes.xlsx")
chemin_fichier_excel3 = os.path.join(bureau, "Vitesses_max.xlsx")

#Enregistrer le DataFrame dans le fichier Excel
df.to_excel(chemin_fichier_excel, index=False) #Excel 1
df2.to_excel(chemin_fichier_excel2, index=False) #Excel 2
df3.to_excel(chemin_fichier_excel3, index=False) #Excel 3
#####
