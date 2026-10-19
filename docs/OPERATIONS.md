# Opérations — runbook pas-à-pas

Qui fait quoi : **Horyon opère** (recherche, rédaction, technique),
**Horeb valide** (choix des cibles, feu vert avant chaque envoi).
Horeb pilote tout depuis le chat, sans coder.

## Étape 1 — Ciblage (Horeb + Horyon)

1. Horeb dit quel type de client viser, ex. *« vise les cybercafés »*.
2. Horyon ouvre `config/icp.json`, choisit ou ajuste le profil correspondant
   et le fait valider par Horeb dans le chat.
3. Résultat : un profil validé (nom, critères, mots-clés, zone).

## Étape 2 — Recherche de prospects (Horyon)

1. Horyon cherche des entreprises correspondant au profil (annuaires, sites,
   Google Maps, réseaux sociaux).
2. Il constitue une liste : entreprise, contact, activité, zone, site web.
3. Il extrait les emails pro publics avec `scripts/find_emails.py` :
   `python3 scripts/find_emails.py urls.txt > emails_trouves.json`
   (1 requête / 2 s, ignore poli des refus 403/429).
4. Il présente la liste à Horeb : *« Voici 30 prospects, tu valides ? »*

## Étape 3 — Rédaction des emails (Horyon)

1. Horyon choisit le template adapté dans `templates/` (1er contact, relance 1, relance 2).
2. Il génère le lot avec `scripts/draft_batch.py` :
   `python3 scripts/draft_batch.py prospects.json templates/email_1_premier_contact.txt`
3. Le lot est écrit dans `queue/batch_YYYYMMDD_HHMMSS.json`, statut **brouillon**.
   **Rien n'est envoyé à ce stade.**
4. Il vérifie l'état avec `scripts/queue_status.py`.

## Étape 4 — VALIDATION HUMAINE (Horeb) — obligatoire

1. Horyon présente le lot dans le chat : nombre d'emails, exemples, cibles.
2. Horeb relit, demande des modifications si besoin, puis dit explicitement
   *« OK envoie »* (ou *« non »* / *« modifie ... »*).
3. Sans ce feu vert explicite : **aucun envoi, aucune exception.**

## Étape 5 — Envoi + suivi (Horyon, puis Horeb)

1. Après validation, Horyon envoie le lot via l'API Gmail (volume plafonné,
   voir `docs/GARDE_FOUS.md`), statut des emails → `envoye`.
2. Il surveille les réponses : résumé de chacune, détection des prospects
   **chauds**.
3. Il relance les prospects tièdes (templates de relance, toujours après
   validation d'Horeb pour chaque vague).
4. Il signale à Horeb : *« 3 prospects chauds à rappeler »* — **Horeb close**.

## Commandes utiles

```bash
python3 scripts/find_emails.py urls.txt > emails_trouves.json
python3 scripts/draft_batch.py prospects.json templates/email_1_premier_contact.txt
python3 scripts/queue_status.py
```
