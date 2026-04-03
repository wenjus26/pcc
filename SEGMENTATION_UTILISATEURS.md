# Proposition de Segmentation des Utilisateurs (CustomUser)

Cette proposition détaille la nouvelle structure de segmentation pour le modèle `CustomUser`, conformément aux besoins de classification de la PCC.

## 1. Structure de Segmentation Proposée

On propose d'ajouter un champ `segment` (ou d'enrichir le champ `role`) pour couvrir les 5 catégories suivantes :

| Segment | Label Technique | Description |
| :--- | :--- | :--- |
| **Section 1 : Soutien Participatif** | `SOUTIEN` | Ministres, Hauts Cadres, etc. |
| **Section 2 : Experts du Forum (CA)** | `EXPERT_CA` | Membres du Conseil d’Administration de la PCC. |
| **Section 3 : Experts du Forum (Hors CA)** | `EXPERT_HCA` | Experts de la plateforme ne faisant pas partie du CA. |
| **Section 4 : Talents & Compétences** | `TALENT` | Professionnels, talents et experts locaux. |
| **Section 5 : Diaspora** | `DIASPORA` | Talents et compétences de la diaspora béninoise. |

## 2. Adaptation Technique du Modèle (Django)

Voici comment nous pourrions adapter le modèle `CustomUser` dans `apps/accounts/models.py` :

```python
class CustomUser(AbstractUser):
    # Séries de constantes pour les types d'utilisateur
    SOUTIEN = 'soutien'
    EXPERT_CA = 'expert_ca'
    EXPERT_HCA = 'expert_hca'
    TALENT = 'talent'
    DIASPORA = 'diaspora'
    ADMIN = 'admin' # Pour les super-utilisateurs techniques

    SEGMENT_CHOICES = [
        (SOUTIEN, _('Soutien Participatif (Ministres/Hauts Cadres)')),
        (EXPERT_CA, _('Expert - Conseil d’Administration PCC')),
        (EXPERT_HCA, _('Expert - Hors Conseil d’Administration PCC')),
        (TALENT, _('Talent & Compétence (Local)')),
        (DIASPORA, _('Talent & Compétence (Diaspora)')),
        (ADMIN, _('Administrateur Système')),
    ]

    segment = models.CharField(
        max_length=20,
        choices=SEGMENT_CHOICES,
        default=TALENT,
        verbose_name=_("Segmentation")
    )
    
    # ... autres champs (phone_number, is_verified, etc.)
```

## 3. Implications & Filtrage

L'utilisation de ces segments permettra de :
- Filtrer les listes d'experts dans le "Talent Map" ou la liste des talents.
- Assigner des droits spécifiques (ex: les `EXPERT_CA` pourraient avoir des vues décisionnelles).
- Personnaliser les tableaux de bord selon le segment.

---
**Action Requise :**
Veuillez valider ces intitulés et cette structure technique. Une fois validée, je procéderai à la mise à jour du fichier `models.py` et à la génération des migrations.
