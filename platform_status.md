# Audit et Plan d'Implémentation - Plateforme PCC

Ce document résume l'état actuel des fonctionnalités de la plateforme et propose une roadmap pour l'implémentation des éléments manquants.

## 1. État des Lieux (Audit)

| Fonctionnalité | Statut | Détails |
| :--- | :--- | :--- |
| **Accueil** | ✅ Existe | Hero section, statistiques, derniers talents/opportunités. |
| **Profils Citoyens** | ✅ Existe | Bio, expériences, éducation, compétences. |
| **Opportunités / Projets** | ✅ Existe | Publication d'appels à projets, candidatures. |
| **Événements** | ✅ Existe | Forums, Masterclasses, Conférences. |
| **Multilingue** | ✅ Existe | Support FR / EN via i18n. |
| **Recherche** | ✅ Partiel | Icône présente, portée à affiner. |
| **Reconnaissance** | ✅ Partiel | Upload de diplômes/certificats, vérification admin. |
| **Notifications** | ✅ Partiel | Modèle `Match` en place, interface à développer. |
| **Carte des Compétences** | ❌ Manquant | Pas de visualisation géographique. |
| **Évaluation (Tests)** | ❌ Manquant | Pas de moteur de quiz/évaluation. |
| **MOOCs / Formations** | ❌ Manquant | Ressources simples uniquement. |
| **Forums / Groupes** | ❌ Manquant | Pas d'espace communautaire interactif. |

---

## 2. Plan d'Implémentation des Fonctionnalités Manquantes

### Étape 1 : Cartographie des Compétences

* **Objectif** : Visualiser la répartition des talents par région au Bénin.
* **Actions** :
  * Utiliser `django-cities-light` ou une liste personnalisée des départements du Bénin.
  * Intégrer une librairie JS comme **Leaflet** ou **Chart.js (Geo map)**.
  * Créer une vue API qui agrège le nombre de profils par localisation.

### Étape 2 : Système d'Évaluation (Tests)

* **Objectif** : Permettre l'auto-évaluation ou la certification des compétences.
* **Actions** :
  * Créer un nouveau module `apps.evaluations`.
  * Modèles : `Quiz`, `Question`, `Option`, `UserResult`.
  * Intégrer des badges de réussite sur le profil citoyen après validation d'un test.

### Étape 3 : Ressources Éducatives (MOOCs)

* **Objectif** : Passer de simples fichiers à des parcours de formation.
* **Actions** :
  * Transformer le modèle `Resource` pour supporter des types "Vidéo" (embed YouTube/Vimeo).
  * Créer des modèles `Course` et `Lesson`.
  * Ajouter un suivi de progression pour les membres.

### Étape 4 : Forum & Communauté

* **Objectif** : Favoriser les échanges thématiques.
* **Actions** :
  * Intégrer `django-machina` (complet) ou développer un module simple de `Threads` et `Comments`.
  * Permettre la création de groupes par catégorie de compétences.

---

## 3. Nouvelle Structure du Menu (À implémenter dans base.html)

La navigation sera réorganisée selon les axes suivants :

* **Accueil** : Présentation, Mission et Chiffres clés.
* **Compétences** : Explorer, Carte (Planifié), Évaluation (Planifié).
* **Projets** : Initiatives citoyennes, Volontariat, Appels.
* **Ressources** : Formations, Guides, Articles.
* **Communauté** : Profils, Groupes (Planifié), Événements.
* **À propos** : Valeurs, Partenaires, Contact.
