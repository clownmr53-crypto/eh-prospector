#!/usr/bin/env python3
"""Affiche l'état des lots d'emails en attente de validation.

Exemple :
    python3 scripts/queue_status.py
"""
import json
from pathlib import Path

QUEUE = Path(__file__).resolve().parent.parent / "queue"


def main():
    batches = sorted(QUEUE.glob("batch_*.json"))
    if not batches:
        print("Aucun lot en file d'attente.")
        return
    for b in batches:
        data = json.loads(b.read_text(encoding="utf-8"))
        emails = data.get("emails", [])
        par_statut = {}
        for e in emails:
            par_statut[e.get("statut", "?")] = par_statut.get(e.get("statut", "?"), 0) + 1
        print(f"- {b.name}")
        print(f"    template : {data.get('template')}")
        print(f"    créé le  : {data.get('created_at')}")
        print(f"    statut   : {data.get('statut')}")
        print(f"    emails   : {len(emails)} {par_statut}")


if __name__ == "__main__":
    main()
