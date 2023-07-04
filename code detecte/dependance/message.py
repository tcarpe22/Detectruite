import os
import plyer
import winsound
import sys

# Obtient le chemin du répertoire du script Python
repertoire = os.path.dirname(os.path.abspath(__file__))

# Normalise le chemin pour obtenir des barres obliques
repertoire = os.path.normpath(repertoire)

def show_notification():
    plyer.notification.notify(
        title='Installation réussie !',
        message='vous êtes prêt à jouer avec des truite. Bon appétit 😉',
        app_icon=f'{repertoire}/event/truite.ico',  # Chemin vers une icône personnalisée si nécessaire
        timeout=10,  # Durée d'affichage de la notification en secondes
        ticker='Notification',  # Texte court qui apparaît brièvement sur certaines plateformes
        toast=True,  # Utiliser les notifications "toast" sur Windows 10
    )
    winsound.PlaySound(f'{repertoire}/event/sound.wav', winsound.SND_FILENAME)

# Appeler la fonction pour afficher la notification et jouer le son
show_notification()
sys.exit()
