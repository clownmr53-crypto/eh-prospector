# Garde-fous — règles non négociables

Ces règles protègent Electronic HOUSE : sa réputation, ses adresses email,
ses numéros WhatsApp et sa conformité légale. Elles s'appliquent à chaque
campagne, sans exception.

## 1. Légalité et respect des personnes

- On contacte uniquement des **adresses email professionnelles affichées
  publiquement** (pages contact, mentions légales, annuaires d'entreprises).
- **Interdit** : récolte massive d'emails personnels, contournement de
  protections anti-scraping, violation des conditions d'utilisation des sites.
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
