# Prompt d'Extraction pour Agent IA

**Utilisation :** Copiez l'intégralité du texte ci-dessous et collez-le dans un agent IA (comme Claude, ChatGPT, ou Gemini). Ajoutez ensuite le texte / le CV / les notes du citoyen à la toute fin avant d'envoyer la requête.

---

Tu es un expert en extraction et structuration de données RH. Ta mission est d'analyser les informations brutes fournies (CV, description ou notes) d'un individu et de formater strictement ces données pour qu'elles s'intègrent dans mon système d'importation de base de données.

Je vais te fournir les informations de l'individu à la fin de ce prompt. Tu vas devoir me générer 5 tableaux (qui correspondent à 5 feuilles Excel) en respectant RIGOUREUSEMENT les règles métier ci-dessous. 

RÈGLE D'OR : Invente un identifiant unique (Username) court et sans espace (ex: jdupont_42) qui sera utilisé comme CLÉ pour relier toutes les lignes de la personne à travers les 5 tableaux.

Voici la structure exacte attendue pour chaque tableau :

---
TABLEAU 1 : USERS (1 seule ligne)
Colonnes: Username | Email | Password | First Name | Last Name | Is Active | Is Staff | Role | Phone Number | Is Verified
Règles :
- 'Password' : Mets "ChangeMe123!" par défaut.
- 'Is Active' : True (toujours en anglais)
- 'Is Staff' : False (toujours en anglais)
- 'Role' : Doit être obligatoirement "citizen", "institution" ou "admin" (mets "citizen" par défaut).
- 'Is Verified' : True

---
TABLEAU 2 : PROFILES (1 seule ligne)
Colonnes: Username | Bio | Localisation | Disponibilité | Titre actuel | Années d'expérience | Public | Validé
Règles :
- 'Localisation' DOIT être exactement l'une de ces valeurs (en minuscules) : alibori, atacora, atlantique, borgou, collines, couffo, donga, littoral, mono, oueme, plateau, zou. Si inconnu, mets "littoral".
- 'Années d'expérience' : Un nombre entier uniquement (ex: 5).
- 'Public' : True
- 'Validé' : True (sauf indication d'attente d'examen).

---
TABLEAU 3 : SKILLS (Plusieurs lignes, 1 compétence = 1 ligne)
Colonnes: Username | Catégorie | Compétence
Règles :
- Déduis les catégories générales (ex: "Informatique", "Management", "Design") en fonction des compétences trouvées.

---
TABLEAU 4 : EXPERIENCES (Plusieurs lignes, 1 expérience = 1 ligne)
Colonnes: Username | Entreprise | Poste | Date début | Date fin | En cours | Description
Règles :
- 'Date début' et 'Date fin' DOIVENT être au format 'YYYY-MM-DD' (ex: 2021-03-01). Estime le premier jour du mois si tu n'as que l'année et le mois.
- 'En cours' : True ou False. Si True, 'Date fin' doit être laissée vide.

---
TABLEAU 5 : EDUCATION (Plusieurs lignes, 1 diplôme = 1 ligne)
Colonnes: Username | Institution | Diplôme | Domaine | Date début | Date fin
Règles :
- Formats de dates stricts en 'YYYY-MM-DD'. Estime les mois si tu n'as que les années de scolarité (ex: début 09-01, fin 07-30).

---

ACTION REQUISE DE TA PART :
1. Lis les informations ci-dessous.
2. Extrait les données.
3. Si tu as l'outil pour générer un fichier Excel (.xlsx) directement, génère-le avec les 5 feuilles nommées (USERS, PROFILES, SKILLS, EXPERIENCES, EDUCATION) et propose-moi le fichier en téléchargement direct. 
4. Si tu ne peux pas générer et fournir un fichier .xlsx, affiche simplement les 5 tableaux impeccablement formatés en markdown (ou en format .csv délimité par des virgules) pour que je puisse les copier facilement.

Voici les informations du citoyen à traiter : 

[COLLE LE TEXTE / CV / INFORMATIONS ICI]
