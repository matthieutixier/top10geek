# -*- coding: utf-8 -*-
"""Garde-fou à l'import des notes presse (décision de Matthieu du 20/11/2026).

Aucune note chiffrée n'entre dans data.json sans avoir été lue sur la page du média lui-même (champ « verifie »).
Une note qui arrive d'un agrégateur (CommentChoisir via build_new.py) ou d'un fichier d'ajout sans preuve de lecture
(ajout_tests.py) est mise « en attente » :
    score = None              -> le test est cité, mais sa note n'entre ni dans la moyenne ni dans le nombre de notes ;
    score_import = <la note>  -> la valeur annoncée par la source, gardée pour mémoire ;
    a_confirmer = JJ/MM/AAAA  -> date de mise en attente.
Elle en sort par presse_crawl.py :
    verifier --ids <produits>  puis  appliquer --apply   (note déclarée en JSON-LD par la page du média), ou
    confirmer <fichier> --apply                          (note lue à la main sur la page du média).
Les notes déjà présentes avant cette règle ne sont pas touchées (elles sont confirmées au fil du relevé à la source).
"""

ATTENTE = ("score_import", "a_confirmer")


def mettre_en_attente(n, jour):
    """Retire la note chiffrée d'un test non lu à la source (la valeur reste dans score_import)."""
    if n.get("score") is None or n.get("verifie"):
        return False
    n["score_import"] = n["score"]
    n["score"] = None
    n["a_confirmer"] = jour
    return True


def sortir_attente(n):
    """À appeler quand la note vient d'être lue sur la page du média."""
    for f in ATTENTE:
        n.pop(f, None)


def controler_import(new_press, old_press, jour):
    """Compare les notes reconstruites (catalogue / cc_fiches) à celles de data.json et applique la règle.
    - note déjà confirmée à la source (verifie) : sa valeur confirmée l'emporte sur celle du catalogue ;
    - note en attente déjà connue : reste en attente ;
    - note ancienne, identique, non confirmée : inchangée (antérieure à la règle) ;
    - note ancienne que la source modifie sans confirmation : la valeur publiée est gardée (écart signalé) ;
    - nouveau test noté : mis en attente.
    Renvoie la liste des (média, détail) à signaler."""
    anciens = {n["url"]: n for n in (old_press or {}).get("notes", [])}
    attente = []
    for n in new_press["notes"]:
        o = anciens.get(n["url"])
        if o and o.get("verifie"):
            for f in ("score", "verifie", "avant", "corrige", "date"):
                if f in o:
                    n[f] = o[f]
            sortir_attente(n)
            continue
        if o and o.get("a_confirmer"):
            for f in ATTENTE:
                n[f] = o[f]
            n["score"] = None
            continue
        if o and o.get("score") == n.get("score"):
            continue
        if o:
            # note déjà publiée, que la source voudrait changer sans lecture à la source : la valeur publiée reste
            attente.append((n["src"], f"{n.get('score')} dans la source, {o.get('score')} gardé"))
            for f in ("score", "avant", "corrige", "date"):
                if f in o:
                    n[f] = o[f]
            continue
        if mettre_en_attente(n, jour):
            attente.append((n["src"], f"{n['score_import']} en attente"))
    return attente


def recalc(pr):
    notes = pr["notes"]
    notes.sort(key=lambda n: (n["score"] is None, -(n["score"] or 0), n["src"]))
    scored = [n for n in notes if n["score"] is not None]
    pr.update(avg=(sum(n["score"] for n in scored) / len(scored)) if scored else None, n=len(scored), tests=len(notes))
