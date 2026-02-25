# AgriSmart IoT - Système de Culture Post-Apocalyptique 🌱☢️

AgriSmart est un système de culture automatisé IoT conçu pour faire pousser de la nourriture (plantes comestibles, ex: haricots) de manière autonome. Ce projet a été développé pour assurer un fonctionnement continu sur une période de 2 semaines, maximiser la vitesse de croissance, et favoriser l'autosuffisance alimentaire dans un contexte post-apocalyptique. Le jardin est physiquement conçu pour accueillir un minimum de 4 capsules de type K-Cup.

## 🌟 Fonctionnalités Principales

*   **💧 Arrosage Automatisé (Hystérésis)** : La pompe à eau s'active automatiquement dès que le système détecte un niveau de sécheresse critique (humidité < 30%) et s'arrête lorsque la terre est de nouveau humide (> 60%). Ceci empêche le "bégaiement" de la pompe et maintient un niveau d'eau optimal. Un mode manuel est également disponible depuis l'application web.
*   **💡 Éclairage Intelligent et Rythme Circadien** :
    *   **5h à 12h (Matin) :** Éclairage Intense (100% de la lampe de croissance).
    *   **12h à 17h (Après-midi) :** Éclairage Modéré (50%).
    *   **17h à 5h (Nuit) :** Éclairage éteint (0%) pour imiter le cycle de repos naturel de la plante.
    *   **Override Capteur :** Si le capteur de luminosité (LDR) détecte une obscurité anormale pendant la journée, la lampe de croissance s'allume automatiquement pour compenser.
*   **🚥 Monitoring Local (LCD & LEDs)** : 
    *   **LCD I2C** : Affiche en temps réel l'heure, la température (°C), l'humidité (%) et l'état du système. En cas d'anomalie de l'IA ou de panne, l'écran affiche un code d'erreur explicite.
    *   **Indicateurs LEDs** : Vert (Système Normal), Orange (Avertissement: Pluie ou Forte Humidité), Rouge (Erreur Critique: Panne DHT11 ou IA).
*   **🧠 Intelligence Artificielle Embarquée** : Un modèle de *Machine Learning* non-supervisé (IsolationForest de Scikit-Learn) analyse le croisement des données (Température, Humidité de l'air, Humidité de l'eau, Luminosité) en temps réel pour détecter des anomalies environnementales complexes (ex: Trop chaud + Très humide => Risque accru de moisissure silencieuse).
*   **🌐 Dashboard Web Sécurisé** : Interface React moderne connectée en temps réel via WebSockets MQTT. Elle exige une authentification (Login/Mot de passe) et permet de visualiser les métriques, l'historique et de prendre le contrôle manuel (forcer l'éclairage ou la pompe).

## 📊 Règles et Seuils de Sécurité (LEDs)

Le système utilise trois LEDs pour indiquer visuellement l'état de santé du jardin intelligent, obéissant à un arbre de décision strict :

2.  🔴 **LED ROUGE (Danger imminent / Manque d'eau / Panne)** - *Priorité Absolue*
    *   **Sol Sec** : Le capteur d'eau détecte une forte sécheresse (ADC >= 150).
    *   **Panne Matérielle** : Le capteur de température/humidité (DHT11) ne répond plus.
    *   **Anomalie IA** : L'algorithme détecte une condition hostile mortelle pour les plants.
3.  🟠 **LED ORANGE (Avertissement mineur)** - *Priorité Secondaire*
    *   **Sol très / trop mouillé** : Le niveau d'eau est considéré comme saturé (ADC < 80).
    *   **Risque de Champignons** : L'humidité de l'air ambiant est extrêmement élevée (> 85%).
4.  🟢 **LED VERTE (Conditions parfaites)** - *État Idéal*
    *   Le sol est **moyennement mouillé**, un niveau idéal pour la plante (ADC entre 80 et 149).
    *   L'air et la température sont à des niveaux sains.
    *   L'IA ne signale aucun danger.

## 🛠 Matériel Requis

*   1x Raspberry Pi (3/4/Zero W)
*   1x Capteur de Température et Humidité (DHT11)
*   1x Capteur de luminosité type LDR (montage RC ou module)
*   1x Capteur de niveau d'eau / pluie analogique connecté via un convertisseur ADC I2C (PCF8591)
*   1x Relais 5V et 1x Mini-pompe à eau submersible
*   1x Lampe de croissance LED (Grow Light)
*   3x LEDs (Vert, Orange, Rouge) + Résistances (220/330 ohms)
*   1x Écran LCD 16x2 avec module I2C
*   Structure pour 4+ capsules K-Cup

## 🚀 Installation & Lancement

1.  **Configuration du Broker MQTT (Securisé)** : 
    Installez Mosquitto sur le Raspberry Pi et mettez en place la configuration fournie avec un mot de passe fort.
    ```bash
    sudo apt install mosquitto mosquitto-clients
    sudo cp iot/smartgarden.conf /etc/mosquitto/conf.d/
    sudo mosquitto_passwd -c /etc/mosquitto/passwd smartgarden
    sudo systemctl restart mosquitto
    ```

2.  **Lancement du Serveur IoT (Python)** :
    ```bash
    cd iot
    pip install -r requirements.txt
    python main.py
    ```

3.  **Lancement du Dashboard Web (React)** :
    ```bash
    cd frontend
    npm install
    npm start
    ```
    *Identifiants par défaut du dashboard : `smartgarden` / `smart2024`*
