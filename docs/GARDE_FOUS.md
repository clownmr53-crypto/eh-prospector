# Garde-fous — règles non négociables

Ces règles protègent Electronic HOUSE : sa réputation, ses adresses email,
ses numéros WhatsApp et sa conformité légale. Elles s'appliquent à chaque
campagne, sans exception.

## 1. Légalité et respect des personnes

- On contacte uniquement des **adresses email professionnelles affichées
  publiquement** (pages contact, mentions légales, annuaires d'entreprises).
- **Interdit** : récolte massive d'emails personnels, contournement de
  protections anti-scraping, violation des conditions d'utilisation des sites.

### 1bis. Particuliers : emails publiés volontairement uniquement.
- Par défaut, les adresses email des **particuliers ne sont pas récoltables** :
  elles ne sont en général pas publiques, et les utiliser pour prospecter
  serait du spam illégal (vie privée, lois anti-spam).
- **Exception autorisée** : on peut collecter l'adresse email d'un
  particulier **uniquement si la personne l'a publiée volontairement
  elle-même** — ex. email affiché dans une annonce, un post public, une
  page pro. Voir la section « email B2C » de `docs/PROSPECTION-B2C.md`.
- **INTERDIT** dans tous les cas :
  - extraire des emails derrière une connexion ou un compte (profils privés,
    messageries, espaces membres) ;
  - contourner des protections anti-scraping ou anti-bot ;
  - violer les conditions d'utilisation (CGU) des sites ;
  - acheter des bases de données d'emails.
- Le cœur du bot email reste **B2B** (revendeurs, entreprises, cybercafés,
  hôtels/ONG). `scripts/find_emails.py` ne s'utilise que sur des pages
  publiques où l'email est affiché volontairement — jamais de crawl
  automatisé de profils.
- Chaque email contient un **lien de désinscription** fonctionnel, et toute
  demande de désinscription est traitée sous 48 h (statut `desinscrit` en base).
- Les relances s'arrêtent dès qu'un prospect dit non ou se désinscrit —
  maximum 2 relances, espacées de plusieurs jours, ton toujours poli.

## 2. Anti-spam

- **Aucun envoi sans le feu vert explicite d'Horeb dans le chat**, lot par lot.
- Prospection **ciblée** uniquement : on écrit à des entreprises choisies pour
  leur pertinence, jamais à des listes achetées ou aspirées en masse.
- Pas d'objets trompeurs (« Re: » uniquement si c'est vraiment une relance
  d'un fil existant), pas de fausses promesses dans le contenu.
- **WhatsApp : jamais d'envoi massif non sollicité.** WhatsApp bannit les
  numéros qui démarchent en masse — les lignes 53/59 sont vitales pour le
  business. Voir le playbook `docs/PROSPECTION-B2C.md`.

## 3. Réputation d'envoi

- **Jamais d'envoi massif depuis l'adresse principale** d'Electronic HOUSE.
- Utiliser un **domaine dédié** à la prospection (ex. `contact-eh.example`),
  avec SPF, DKIM et DMARC configurés.
- **Warmup progressif** : commencer à 20-50 emails/jour, augmenter
  graduellement sur plusieurs semaines en surveillant les rebonds et les
  signalements spam.
- Plafonds : pas plus de ~200 emails/jour par domaine tant que la réputation
  n'est pas établie ; pause immédiate si le taux de rebond dépasse 5 % ou si
  des signalements spam apparaissent.
- Surveiller la délivrabilité (dossiers spam, blacklists) avant chaque montée
  en volume.

## 4. Données

- On ne stocke que le minimum utile : nom d'entreprise, contact, email pro,
  activité, statut. Pas de données personnelles sensibles.
- Aucun secret, token ou mot de passe dans ce repo ni dans les scripts.
- Les exports de prospects restent internes à Electronic HOUSE.
