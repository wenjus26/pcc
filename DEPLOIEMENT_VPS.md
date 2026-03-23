# 🚀 Guide de Préparation du VPS pour Déploiement

Avant d'exécuter `git add`, `git commit` et `git push` pour mettre votre projet en ligne pour la première fois, vous devez préparer votre serveur VPS et l'environnement GitHub pour qu'ils puissent communiquer correctement.

Voici les 5 étapes cruciales à réaliser.

---

## 🌐 Étape 1 : Configurer votre nom de domaine
Allez sur l'interface de votre fournisseur de nom de domaine (où vous avez acheté ou géré `beninsoya.com`).
Modifiez les paramètres DNS de votre domaine (Zone DNS) pour ajouter un enregistrement de type **A** :
- **Nom (Host)**: `pcc`
- **Valeur / Cible (Target)**: `L'adresse IP de votre VPS` (ex: `197.234...`)
- *Laissez le temps aux serveurs DNS de se propager (cela peut prendre de 5 à 30 minutes).*

---

## 🛠 Étape 2 : Préparer le système du VPS (Docker & Dossiers)
Connectez-vous à votre VPS via SSH en tant qu'utilisateur `ubuntu` :
```bash
ssh ubuntu@ADRESSE_IP_DE_VOTRE_VPS
```

Exécutez ensuite les commandes suivantes pour installer Docker et créer les dossiers :
```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Docker et Docker Compose
sudo apt-get install ca-certificates curl gnupg lsb-release -y
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Donner les droits Docker à votre utilisateur (ubuntu)
sudo usermod -aG docker $USER
```

*Remarque : Tapez `exit` puis reconnectez-vous au VPS en SSH pour que les permissions de groupe Docker s'appliquent.*

Ensuite, préparez le répertoire principal du site web :
```bash
sudo mkdir -p /var/www/pcc
sudo chown -R $USER:$USER /var/www/pcc
```

---

## 🔑 Étape 3 : Configurer les clés SSH pour GitHub Actions
C'est indispensable pour que GitHub puisse envoyer le code sur votre serveur de façon sécurisée et automatisée.

**1. Sur votre VPS, générez une nouvelle clé SSH spécialement pour le déploiement :**
```bash
ssh-keygen -t ed25519 -f ~/.ssh/github_deploy_key -N ""
```

**2. Autorisez cette clé sur votre VPS :**
```bash
cat ~/.ssh/github_deploy_key.pub >> ~/.ssh/authorized_keys
```

**3. Configurez les "Secrets" sur le site GitHub :**
Affichez le contenu de votre clé **PRIVÉE** et copiez ABSOLUMENT TOUT le bloc (y compris les lignes "BEGIN" et "END") :
```bash
cat ~/.ssh/github_deploy_key
```

Allez sur votre dépôt web : **GitHub.com > Votre Projet (wenjus26/pcc) > Settings > Secrets and variables > Actions > New repository secret**.

Ajoutez ces 3 secrets en respectant scrupuleusement les majuscules :
- Nom : `VPS_HOST` | Valeur : *L'adresse IP de votre VPS*
- Nom : `VPS_USER` | Valeur : `ubuntu`
- Nom : `VPS_SSH_KEY` | Valeur : *Le contenu collé de votre clé privée*

---

## 🔐 Étape 4 : Créer le fichier des variables d'environnement sur le VPS
Votre serveur a besoin de mots de passe pour sécuriser sa propre base de données.

Toujours sur votre VPS, exécutez ces commandes :
```bash
cd /var/www/pcc
nano .env
```

Collez le contenu suivant dans le fichier. **Modifiez les mots de passe** par des valeurs sûres !
```env
# --- Production Configuration (MySQL) ---
DEBUG=False
SECRET_KEY=REMPLACEZ_MOI_PAR_UNE_CLE_TRES_LONGUE_ET_SANS_ESPACES
DATABASE_URL=mysql://pcc_user:VOTRE_MOT_DE_PASSE_SQL_ICI@db:3306/pcc_db
ALLOWED_HOSTS=localhost,127.0.0.1,pcc.beninsoya.com

# --- Security Settings (HTTPS) ---
CSRF_TRUSTED_ORIGINS=https://pcc.beninsoya.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# --- Static & Media Files ---
USE_WHITENOISE=True
COMPRESS_STORAGE=True
```
*Pour enregistrer dans Nano : Faites `Ctrl+O`, appuyez sur `Entrée`, puis quittez avec `Ctrl+X`.*

---

## 🎉 Étape Finale : LANCER VOTRE PREMIER DÉPLOIEMENT

Maintenant que tout est vérifié :
1. Sur votre **PC Local Windows** (dans VS Code par exemple), exécutez ces commandes :
```bash
git add .
git commit -m "Déploiement initial Production CI/CD"
git push origin main
```
2. Allez sur **GitHub dans l'onglet "Actions"**. Attendez de voir la barre de progression se terminer (icône verte).

---

> ⚠️ **ATTENTION : Certificats HTTPS (TRÈS IMPORTANT)** ⚠️
>
> Lors du TOUT PREMIER lancement, la sécurité Nginx (certbot) bloquera le démarrage car le certificat SSL n'est pas encore réellement créé.
> 
> *Une fois que votre `git push` a réussi sur GitHub*, retournez sur votre VPS et tapez ces DEUX commandes obligatoires en SSH pour initialiser le "cadenas vert" officiel :
>
> ```bash
> cd /var/www/pcc
> docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d pcc.beninsoya.com --email VOTRE_ADRESSE_EMAIL_PERSO@GMAIL.COM --agree-tos --no-eff-email
> docker compose restart nginx
> ```

**Félicitations, votre projet sera en ligne, professionnel, rapide et ultra sécurisé !** 🚀
