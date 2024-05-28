# Installation et Initialisation du Projet

Ce document explique les étapes nécessaires pour installer et initialiser le projet.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- Python (version X.X.X)
- pip (version X.X.X)

## Étapes

1. Cloner le projet depuis le référentiel GitHub :

    ```bash
    git clone https://github.com/TimomoCorn/generate_flight_dataset.git
    ```

2. Accéder au répertoire du projet :

    ```bash
    cd gerenate_flight_dataset
    ```

3. Créer un environnement virtuel Python :

    ```bash
    python -m venv .env
    ```

4. Activer l'environnement virtuel :

    - Sur Windows :

      ```bash
      .env\Scripts\activate
      ```

    - Sur macOS et Linux :

      ```bash
      source .env/bin/activate
      ```

5. Installer les dépendances du projet à partir du fichier `requirements.txt` :

    ```bash
    pip install -r requirements.txt
    ```

6. Lancer le programme :

    ```bash
    python main.py
    ```

C'est tout! Vous avez maintenant installé et initialisé le projet avec succès. Désormais, un jeu de données d'exemple est disponible pour visualiser facilement les différents cas du projet dans le dossier `data`.
