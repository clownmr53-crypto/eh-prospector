#!/usr/bin/env python3
"""Génère un lot d'emails de prospection personnalisés à partir d'un template.

- Lit config/icp.json (pour info) + une liste de prospects en JSON.
- Remplit les placeholders {{prenom}}, {{entreprise}}, {{activite}}, {{produit}}, {{lien_desinscription}}.
- Écrit le lot dans queue/batch_YYYYMMDD_HHMMSS.json au statut "brouillon".
- N'ENVOIE RIEN : l'envoi n'a lieu qu'après validation d'Horeb dans le chat.

Format attendu du fichier prospects (JSON) : une liste d'objets, ex.
[
  {"entreprise": "Tech SARL", "prenom": "Aïcha", "email": "contact@tech.example",
   "activite": "vente de téléphones", "produit": "téléphones et accessoires"}
]

Exemple :
    python3 scripts/draft_batch.py prospects.json templates/email_1_premier_contact.txt
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
QUEUE = BASE / "queue"
PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")
DESINSCRIPTION_BASE = "https://electronichouse.example/desinscription?e="


def render(template_text: str, prospect: dict) -> str:
    data = dict(prospect)
    # lien de désinscription : placeholder technique, remplacé ici par une valeur par défaut
    data.setdefault("lien_desinscription", DESINSCRIPTION_BASE + "{{email}}")
    data["lien_desinscription"] = data["lien_desinscription"].replace(
        "{{email}}", prospect.get("email", "")
    )

    def repl(m):
        return str(data.get(m.group(1), f"[{m.group(1)}]"))

    return PLACEHOLDER_RE.sub(repl, template_text)


def main():
    if len(sys.argv) != 3:
        print("Usage : python3 scripts/draft_batch.py <prospects.json> <template.txt>",
              file=sys.stderr)
        sys.exit(1)

    prospects = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    template_text = Path(sys.argv[2]).read_text(encoding="utf-8")
    template_name = Path(sys.argv[2]).stem

    # La première ligne "OBJET : ..." du template devient l'objet de l'email
    first, _, body = template_text.partition("\n")
    objet = first.replace("OBJET :", "").strip() if first.startswith("OBJET") else "(sans objet)"

    batch = {
        "template": template_name,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "statut": "brouillon",
        "note": "EN ATTENTE DE VALIDATION D'HOREB — aucun envoi effectué.",
        "emails": [],
    }
    for p in prospects:
        batch["emails"].append({
            "prospect": p.get("entreprise"),
            "email": p.get("email"),
            "objet": render(objet, p),
            "corps": render(body, p),
            "statut": "brouillon",
        })

    QUEUE.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = QUEUE / f"batch_{stamp}.json"
    out.write_text(json.dumps(batch, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Lot généré : {out} ({len(batch['emails'])} emails, statut=brouillon)")
    print("Rappel : AUCUN email envoyé. Présenter le lot à Horeb pour validation.")


if __name__ == "__main__":
    main()
