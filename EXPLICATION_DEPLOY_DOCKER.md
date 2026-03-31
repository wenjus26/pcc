# Rapport de Déploiement : Mise à jour Docker (PCC)

Ce document explique en détail les opérations effectuées dans votre terminal lors du déploiement de la plateforme **PCC** sur le VPS.

---

## 1. Résolution de l'incident de répertoire

**Commande :** `sudo docker-compose down` (exécutée dans `/etc/nginx/sites-available/`)
**Résultat :** `ERROR: Can't find a suitable configuration file...`

*   **Analyse :** Docker ne trouvait pas le fichier `docker-compose.yml`.
*   **Action corrective :** Vous avez utilisé `cd /var/www/pcc` pour vous placer à la racine du projet. La commande `ls` a confirmé la présence des fichiers nécessaires (`Dockerfile`, `docker-compose.yml`, etc.).

## 2. Redémarrage et Re-construction

**Commande :** `sudo docker-compose up -d --build`

L'option `--build` est cruciale ici car elle demande à Docker de ne pas utiliser l'ancienne image mais d'en créer une nouvelle avec votre code mis à jour.

### Étape par étape : La phase de "Build"

#### A. Environnement de Base (Steps 1-4)

```docker
Step 1/12 : FROM python:3.12-slim-bullseye
```

Docker télécharge une version légère de Debian (Bullseye) optimisée pour Python 3.12. C'est le socle de votre application.

#### B. Dépendances Système (Step 5)

```docker
RUN apt-get update && apt-get install -y ...
```

Cette étape installe les outils nécessaires pour compiler les bibliothèques Python complexes :

*   `build-essential` : Compilateur GCC.
*   `libpq-dev` & `default-libmysqlclient-dev` : Connecteurs pour PostgreSQL et MySQL/MariaDB.
*   `gettext` : Outil pour la gestion des traductions du site.

*Note :* On voit dans les logs que Docker a téléchargé 86.4 Mo de paquets système.

#### C. Dépendances Python (Steps 6-7)

```docker
RUN pip install --no-cache-dir -r requirements.txt
```

C'est ici que votre environnement Django est créé. On observe l'installation de :

*   **Django 5.1.15** (Cœur du site)
*   **mysqlclient 2.2.8** (Lien avec la base MariaDB)
*   **Pillow 12.1.1** (Gestion des images)
*   **Gunicorn 25.3.0** (Serveur de production)
*   **WhiteNoise 6.12.0** (Gestion des fichiers statiques CSS/JS)

#### D. Finalisation (Steps 8-12)

Docker copie votre code (`COPY . .`), définit le port d'entrée (**8013**) et configure le script de démarrage (`entrypoint.sh`).

## 3. Mise en service

```bash
Creating pcc_db ... done
Creating pcc_web ... done
```

**Situation finale :**

1.  **pcc_db** : Votre conteneur de base de données est opérationnel.
2.  **pcc_web** : Votre application Django tourne en arrière-plan (mode `-d` déconnecté).
3.  **Nettoyage** : Docker a supprimé les conteneurs intermédiaires utilisés pendant la construction pour économiser de l'espace.

---

> [!IMPORTANT]
> **Points de succès :**
> *   Le passage de Python 3.12-slim est validé.
> *   Toutes les migrations et collectes de fichiers statiques (via entrypoint) ont dû s'exécuter normalement.
> *   Le site est maintenant accessible via le proxy inverse Nginx.
