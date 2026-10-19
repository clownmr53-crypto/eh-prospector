# eh-prospector — Bot de prospection d'Electronic HOUSE

Ce bot aide Electronic HOUSE à trouver de nouveaux clients, **pros comme
particuliers**, de façon ciblée et respectueuse. Deux volets :

- **Email → les pros** : revendeurs, entreprises, cybercafés, hôtels/ONG.
  C'est là que l'email fonctionne. Chaque vague d'emails est **validée par
  Horeb dans le chat** avant de partir — jamais d'envoi massif sauvage.
- **WhatsApp → les particuliers** : listes opt-in, groupes Facebook,
  statuts WhatsApp, parrainage. Jamais de démarchage massif (risque de ban
  du numéro). Les particuliers peuvent aussi être contactés par email
  **uniquement s'ils ont publié leur adresse eux-mêmes** (annonce, post
  public).

## Volet email (pros) — workflow en 5 étapes

1. **Ciblage** — On définit ensemble le profil du client idéal
   (voir `config/icp.json`). Exemple : les revendeurs de téléphones au Bénin.
2. **Recherche** — Le bot cherche des entreprises qui correspondent à ce
   profil sur le web (annuaires, sites d'entreprises, Google Maps...).
3. **Emails** — Il récupère uniquement les adresses email **affichées
   publiquement et volontairement** (pages contact, mentions légales,
   annonces) puis rédige des emails personnalisés en français.
4. **VALIDATION HUMAINE obligatoire** — Horeb relit chaque lot d'emails dans
   le chat et donne son feu vert. **Aucun email ne part sans sa validation.**
5. **Envoi + suivi** — Une fois validés, les emails partent (volume limité
   et progressif), le bot gère les réponses de façon conversationnelle et
   signale les prospects chauds à Horeb pour qu'il close lui-même.

## Volet WhatsApp (particuliers)

Playbook complet dans `docs/PROSPECTION-B2C.md` : listes opt-in et clients
existants, groupes Facebook, statuts WhatsApp (ligne 53), parrainage.
Modèles de messages courts en français dans `templates/whatsapp/`
(premier contact, relance, offre).

## Garde-fous (non négociables)

- Pas de spam : prospection ciblée uniquement, jamais d'envoi massif.
- Emails : uniquement des adresses affichées publiquement et
  volontairement — jamais d'emails extraits derrière un compte, jamais de
  bases achetées, jamais de contournement de protections.
- Aucun envoi sans le feu vert d'Horeb dans le chat.
- Volume email plafonné et progressif (ex. 20 à 50/jour au début).
- Chaque email contient un lien de désinscription.
- WhatsApp : jamais d'envoi massif non sollicité (ban du numéro).
- Détails complets : voir `docs/GARDE_FOUS.md`.

## Comment Horeb pilote le bot (zéro code)

Tout se passe dans le chat avec Horyon, en langage simple :

- *« Cherche 30 revendeurs de téléphones à Cotonou »* → le bot cherche.
- *« Montre-moi les emails »* → Horyon présente le lot à valider.
- *« OK envoie »* → les emails partent.
- *« Qui a répondu ? »* → Horyon fait le point sur les réponses.
- *« Prépare les statuts WhatsApp de la semaine »* → Horyon les rédige.

Le runbook détaillé est dans `docs/OPERATIONS.md`.

## Contenu du repo

| Dossier / fichier              | Rôle                                              |
|--------------------------------|---------------------------------------------------|
| `config/icp.json`              | Profils de clients idéaux (4 exemples pré-remplis)|
| `templates/`                   | Modèles d'emails : 1er contact + 2 relances        |
| `templates/whatsapp/`          | Modèles WhatsApp : 1er contact, relance, offre     |
| `db/schema.sql`                | Tables Supabase : prospects, campagnes, emails... |
| `scripts/find_emails.py`       | Extraction d'emails publics depuis des URLs       |
| `scripts/draft_batch.py`       | Génération d'un lot d'emails (brouillons, sans envoi) |
| `scripts/queue_status.py`      | État des lots en attente de validation           |
| `docs/GARDE_FOUS.md`           | Règles anti-spam et de réputation d'envoi         |
| `docs/OPERATIONS.md`           | Runbook pas-à-pas du workflow                     |
| `docs/PROSPECTION-B2C.md`      | Playbook particuliers (WhatsApp + email public)   |

## Roadmap

- [x] Socle email B2B : ciblage, recherche, modèles, file de validation
- [x] Volet B2C : playbook WhatsApp + modèles de messages
- [ ] Connexion Supabase (tables `prospects`, `campagnes`, `emails`, `reponses`)
- [ ] Envoi via API Gmail après validation (avec désinscription)
- [ ] Gestion conversationnelle des réponses + détection des prospects chauds
- [ ] Tableau de bord simple (prospects, envoyés, réponses, taux)
- [ ] Domaine d'envoi dédié + warmup progressif
