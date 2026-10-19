#!/usr/bin/env python3
"""Extrait les adresses email affichées publiquement dans le HTML d'une liste d'URLs.

Usage ciblé uniquement : prospection B2B d'Electronic HOUSE.
- Lit un fichier texte contenant une URL par ligne.
- Respecte un délai de 2 secondes entre chaque requête (rate-limit).
- S'identifie avec un user-agent explicite.
- Ignore poliment les pages qui refusent (403/429/erreurs) : on passe à la suivante.
- Affiche les emails trouvés au format JSON sur stdout.

Exemple :
    python3 scripts/find_emails.py urls.txt > emails_trouves.json
"""
import json
import re
import sys
import time
import urllib.request
import urllib.error

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
USER_AGENT = "EH-Prospector/1.0 (prospection B2B Electronic HOUSE ; contact pro uniquement)"
DELAY_SECONDS = 2
TIMEOUT_SECONDS = 15

# Extensions d'images/fichiers à ignorer dans les faux positifs
JUNK_TLDS = {"png", "jpg", "jpeg", "gif", "svg", "webp", "css", "js"}


def extract_emails(html: str):
    found = set()
    for m in EMAIL_RE.findall(html):
        local, _, domain = m.rpartition("@")
        tld = domain.rsplit(".", 1)[-1].lower()
        if tld in JUNK_TLDS:
            continue
        found.add(m.lower())
    return sorted(found)


def fetch(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            ctype = resp.headers.get("Content-Type", "")
            if "html" not in ctype and "text" not in ctype:
                return None, "contenu non textuel, ignoré"
            return resp.read().decode("utf-8", errors="replace"), None
    except urllib.error.HTTPError as e:
        # 403/429/autres refus : on passe poliment à la suivante
        return None, f"HTTP {e.code}, ignoré poliment"
    except Exception as e:  # timeout, DNS, SSL...
        return None, f"erreur ({type(e).__name__}), ignoré"


def main():
    if len(sys.argv) != 2:
        print("Usage : python3 scripts/find_emails.py <fichier_urls.txt>", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        urls = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]

    results = []
    for i, url in enumerate(urls):
        if i > 0:
            time.sleep(DELAY_SECONDS)  # rate-limit : 1 requête / 2 s
        html, err = fetch(url)
        if err:
            results.append({"url": url, "emails": [], "note": err})
            continue
        results.append({"url": url, "emails": extract_emails(html), "note": "ok"})
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
