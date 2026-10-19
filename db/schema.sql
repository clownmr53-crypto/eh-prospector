-- Schéma Supabase pour eh-prospector
-- À exécuter dans l'éditeur SQL de Supabase (projet eh-prod)

create table if not exists prospects (
  id          uuid primary key default gen_random_uuid(),
  entreprise  text not null,
  contact_nom text,
  email       text,
  telephone   text,
  activite    text,
  taille      text,
  site_web    text,
  zone        text,
  source      text,        -- ex: "annuaire", "google_maps", "site_web"
  statut      text not null default 'nouveau'
              check (statut in ('nouveau','contacte','repondu','chaud','client','refuse','desinscrit')),
  created_at  timestamptz not null default now()
);

create table if not exists campagnes (
  id         uuid primary key default gen_random_uuid(),
  nom        text not null,
  icp_ref    text,          -- nom du profil dans config/icp.json
  statut     text not null default 'preparation'
             check (statut in ('preparation','en_validation','approuvee','en_cours','terminee','annulee')),
  created_at timestamptz not null default now()
);

create table if not exists emails (
  id          uuid primary key default gen_random_uuid(),
  campagne_id uuid references campagnes(id) on delete cascade,
  prospect_id uuid references prospects(id) on delete cascade,
  template    text not null, -- ex: "email_1_premier_contact"
  objet       text not null,
  corps       text not null,
  statut      text not null default 'brouillon'
              check (statut in ('brouillon','approuve','envoye','erreur')),
  envoye_le   timestamptz,
  created_at  timestamptz not null default now()
);

create table if not exists reponses (
  id       uuid primary key default gen_random_uuid(),
  email_id uuid references emails(id) on delete cascade,
  recu_le  timestamptz not null default now(),
  resume   text,           -- résumé rédigé par Horyon
  chaud    boolean not null default false
);

create index if not exists idx_prospects_statut on prospects(statut);
create index if not exists idx_emails_statut on emails(statut);
create index if not exists idx_emails_campagne on emails(campagne_id);
