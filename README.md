# eh-prospector — Bot de prospection B2B par email d'Electronic HOUSE

Ce bot aide Electronic HOUSE à trouver de nouveaux clients **professionnels**
(revendeurs, entreprises, cybercafés, hôtels...) par email, de façon ciblée
et respectueuse. Il ne fait jamais d'envoi massif sauvage : chaque vague
d'emails est **validée par Horeb dans le chat** avant de partir.

## Ce que fait le bot

1. **Ciblage** — On définit ensemble le profil du client idéal
   (voir `config/icp.json`). Exemple : les revendeurs de téléphones au Bénin.
2. **Recherche** — Le bot cherche des entreprises qui correspondent à ce
   profil sur le web (annuaires, sites d'entreprises, Google Maps...).
3. **Emails** — Il récupère uniquement les adresses email professionnelles
   **affichées publiquement** (pages contact, mentions légales) puis rédige
   des emails personnalisés en français pour chaque prospect.
4. **VALIDATION HUMAINE obligatoire** — Horeb relit chaque lot d'emails dans
   le chat et donne son feu vert. **Aucun email ne part sans sa validation.**
5. **Envoi + suivi** — Une fois validés, les emails partent (volume limité
   et progressif), le bot gère les réponses de façon conversationnelle et
   signale les prospects chauds à Horeb pour qu'il close lui-même.

## Garde-fous (non négociables)

- Pas de spam : prospection ciblée uniquement, jamais d'envoi massif.
- Uniquement des emails professionnels publics — jamais d'emails personnels
  récoltés en masse.
- Aucun envoi sans le feu vert d'Horeb dans le chat.
- Volume plafonné et progressif (ex. 20 à 50 emails/jour au début).
- Chaque email contient un lien de désinscription.
- Détails complets : voir `docs/GARDE_FOUS.md`.

## Comment Horeb pilote le bot (zéro code)

Tout se passe dans le chat avec Horyon, en langage simple :

- *« Cherche 30 revendeurs de téléphones à Cotonou »* → le bot cherche.
- *« Montre-moi les emails »* → Horyon présente le lot à valider.
- *« OK envoie »* → les emails partent.
- *« Qui a répondu ? »* → Horyon fait le point sur les réponses.

Le runbook détaillé est dans `docs/OPERATIONS.md`.

## Contenu du repo

| Dossier / fichier              | Rôle                                              |
|--------------------------------|---------------------------------------------------|
| `config/icp.json`              | Profils de clients idéaux (4 exemples pré-remplis)|
| `templates/`                   | Modèles d'emails : 1er contact + 2 relances        |
| `db/schema.sql`                | Tables Supabase : prospects, campagnes, emails... |
| `scripts/find_emails.py`       | Extraction d'emails publics depuis des URLs       |
| `scripts/draft_batch.py`       | Génération d'un lot d'emails (brouillons, sans envoi) |
| `scripts/queue_status.py`      | État des lots en attente de validation           |
| `docs/GARDE_FOUS.md`           | Règles anti-spam et de réputation d'envoi         |
| `docs/OPERATIONS.md`           | Runbook pas-à-pas du workflow                     |

## Roadmap

- [x] Socle : ciblage, recherche, modèles d'emails, file de validation
- [ ] Connexion Supabase (tables `prospects`, `campagnes`, `emails`, `reponses`)
- [ ] Envoi via API Gmail après validation (avec désinscription)
- [ ] Gestion conversationnelle des réponses + détection des prospects chauds
- [ ] Tableau de bord simple (prospects, envoyés, réponses, taux)
- [ ] Domaine d'envoi dédié + warmup progressif
