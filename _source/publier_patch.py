#!/usr/bin/env python3.12
"""Publication par fichier de modifications (« patch ») : applique, régénère, contrôle.

Les tâches planifiées n'ont plus d'accès git en écriture : elles déposent sur GitHub un petit fichier
`_publication/<AAAA-MM-JJ>-<tâche>.patch` (un `git diff` des seules sources de données) et
`.github/workflows/publier.yml` lance ce script, qui :

  1. refuse tout patch qui touche autre chose que des données (jamais gen10.py, classement.py, HTML…) ;
  2. applique le patch (`git apply --3way`), remet la date globale `date` de data.json à sa valeur d'avant
     (règle SEO 6 : une date ne bouge que si le contenu a changé) ;
  3. régénère le site (`gen10.py`) ;
  4. contrôle les règles SEO du § 6 bis de CLAUDE.md (indexation, canoniques, H1, lastmod, JSON-LD, sitemap) ;
  5. s'arrête SANS rien publier au premier contrôle qui échoue (code de sortie ≠ 0, raisons affichées).

Le script ne commite rien : c'est le workflow qui commite et pousse si tout est bon.
Usage : python3.12 _source/publier_patch.py <fichier.patch> [--sans-generation]
Codes : 0 = prêt à publier (ou rien à publier), 2 = patch refusé / non applicable, 3 = contrôle SEO échoué,
        4 = génération en erreur.
"""
import json
import os
import re
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RACINE)

# Fichiers qu'un patch de données peut modifier (tout le reste est refusé).
AUTORISES = [
    r"_source/data\.json",
    r"_source/catalog[a-z_]*\.py",
    r"_source/cc_fiches_[a-z_]+\.json",
    r"_source/syntheses[a-z_]*\.json",
    r"_source/historique_prix\.json",
    r"_source/manuel_[a-z_]+\.json",
    r"_source/profiles\.py",
    r"_source/effinity_map\.json",
]
MAX_NOUVELLES_INDEXEES = 30          # règle SEO 4
MAX_PART_LASTMOD = 0.40              # règle SEO 6 : « la plupart des URL » = erreur


def sh(*cmd, check=True, capture=True):
    r = subprocess.run(cmd, capture_output=capture, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} -> {r.returncode}\n{r.stdout}\n{r.stderr}")
    return r


def fin(code, titre, lignes=()):
    print(f"\n=== {titre} ===")
    for l in lignes:
        print(f" - {l}")
    sys.exit(code)


def head_file(path):
    r = sh("git", "show", f"HEAD:{path}", check=False)
    return r.stdout if r.returncode == 0 else None


def sitemap_info(texte):
    urls = {}
    for m in re.finditer(r"<url>\s*<loc>(.*?)</loc>(?:\s*<lastmod>(.*?)</lastmod>)?", texte, re.S):
        urls[m.group(1)] = m.group(2)
    return urls


def pages_noindex(ref):
    """Ensemble des pages HTML marquées noindex (HEAD si ref == 'HEAD', sinon arborescence de travail)."""
    if ref == "HEAD":
        r = sh("git", "grep", "-l", "-E", r'name="robots" content="[^"]*noindex', "HEAD", "--", "*.html", check=False)
        return {l.split(":", 1)[1] for l in r.stdout.splitlines() if ":" in l}
    r = sh("git", "grep", "-l", "--untracked", "-E", r'name="robots" content="[^"]*noindex', "--", "*.html", check=False)
    return set(r.stdout.split())


def extrait(html, motif):
    m = re.search(motif, html, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else None


def ld_blocs(html):
    return re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)


def parcourir(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from parcourir(v)
    elif isinstance(o, list):
        for v in o:
            yield from parcourir(v)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        fin(2, "Usage", ["python3.12 _source/publier_patch.py <fichier.patch>"])
    patch = os.path.abspath(args[0])
    if not os.path.isfile(patch) or os.path.getsize(patch) == 0:
        fin(2, "Patch absent ou vide", [patch])

    if sh("git", "status", "--porcelain").stdout.strip():
        fin(2, "Arborescence non propre : le script doit partir d'un état identique à HEAD",
            sh("git", "status", "--short").stdout.splitlines()[:10])

    # 1. Contrôle des fichiers touchés
    texte = open(patch, encoding="utf-8").read()
    fichiers = re.findall(r"^diff --git a/(\S+) b/(\S+)$", texte, re.M)
    if not fichiers:
        fin(2, "Patch illisible (aucune ligne « diff --git »)")
    refuses = [b for a, b in fichiers if not any(re.fullmatch(p, b) for p in AUTORISES)]
    if refuses:
        fin(2, "Patch refusé : fichiers non autorisés (seules les données sont acceptées)", refuses)
    if "GIT binary patch" in texte:
        fin(2, "Patch refusé : contenu binaire")

    # 2. État avant
    data_avant = json.loads(head_file("_source/data.json"))
    date_avant = data_avant.get("date")
    urls_avant = sitemap_info(head_file("sitemap-v2.xml") or head_file("sitemap.xml") or "")   # sitemap-v2.xml depuis le 13/11/2026
    noindex_avant = pages_noindex("HEAD")
    nb_produits_avant = len(data_avant.get("items", data_avant.get("produits", []))) if isinstance(data_avant, dict) else None

    # 3. Application
    r = sh("git", "apply", "--3way", "--whitespace=nowarn", patch, check=False)
    if r.returncode != 0:
        fin(2, "Le patch ne s'applique pas sur le main actuel (conflit)", (r.stdout + r.stderr).splitlines()[-8:])
    if sh("git", "ls-files", "-u").stdout.strip():
        fin(2, "Conflit de fusion dans le patch", sh("git", "ls-files", "-u").stdout.splitlines()[:6])

    # date globale remise à sa valeur d'avant (règle SEO 6)
    chemin = "_source/data.json"
    d = json.load(open(chemin, encoding="utf-8"))
    if d.get("date") != date_avant:
        d["date"] = date_avant
        open(chemin, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
        print(f"date globale remise à {date_avant}")
    try:
        json.load(open(chemin, encoding="utf-8"))
    except Exception as e:
        fin(2, "data.json illisible après application", [str(e)])

    if "--sans-generation" in sys.argv:
        fin(0, "Patch appliqué (génération sautée)")

    # 4. Génération
    g = sh("python3.12" if sh("which", "python3.12", check=False).returncode == 0 else sys.executable,
           "_source/gen10.py", check=False)
    sortie = (g.stdout + g.stderr).strip().splitlines()
    ok = next((l for l in sortie if l.startswith("OK ")), None)
    if g.returncode != 0 or not ok:
        fin(4, "gen10.py en erreur", sortie[-12:])
    print(ok)
    m = re.match(r"OK (\d+) produits", ok)
    nb_produits = int(m.group(1)) if m else None

    modifs = [l[3:] for l in sh("git", "status", "--porcelain").stdout.splitlines()]
    if not modifs:
        fin(0, "Rien à publier : le patch n'a rien changé (déjà appliqué ?)")
    html_modifies = [f for f in modifs if f.endswith(".html")]

    echecs = []

    # 5. Contrôles SEO
    # 5a. Fichiers modifiés : seulement données, pages générées, sitemap, images réduites
    for f in modifs:
        if f in ("_source/gen10.py", "_source/classement.py", "_source/rivaux.py", "_source/sitemap_v2.json", "_source/rivaux_specs.json", "robots.txt", "_headers", "_redirects"):
            echecs.append(f"fichier protégé modifié : {f}")
        if f.endswith("effinity.local.json") or f.endswith("amazon.local.json"):
            echecs.append(f"fichier secret présent : {f}")

    # 5b. Sitemap (sitemap-v2.xml, noyau figé depuis le 13/11/2026) : aucune URL retirée, aucune ajoutée par une tâche
    urls_apres = sitemap_info(open("sitemap-v2.xml", encoding="utf-8").read()) if os.path.exists("sitemap-v2.xml") else {}
    if not urls_apres:
        echecs.append("sitemap-v2.xml absent ou vide")
    retirees = sorted(set(urls_avant) - set(urls_apres))
    ajoutees = sorted(set(urls_apres) - set(urls_avant))
    if retirees:
        echecs.append(f"{len(retirees)} URL retirée(s) du sitemap (règle 2) : {retirees[:5]}")
    if len(ajoutees) > MAX_NOUVELLES_INDEXEES:
        echecs.append(f"{len(ajoutees)} nouvelles URL au sitemap (maximum {MAX_NOUVELLES_INDEXEES} par publication, règle 4)")

    # 5c. Indexation : aucune page ne passe en noindex (règles 1 à 3)
    noindex_apres = pages_noindex("travail")
    nouveaux_noindex = sorted(noindex_apres - noindex_avant)
    if nouveaux_noindex:
        echecs.append(f"{len(nouveaux_noindex)} page(s) passent en noindex (règle 2) : {nouveaux_noindex[:5]}")
    nouvelles_indexees = sorted(noindex_avant - noindex_apres)
    if len(nouvelles_indexees) > MAX_NOUVELLES_INDEXEES:
        echecs.append(f"{len(nouvelles_indexees)} pages deviennent indexables (maximum {MAX_NOUVELLES_INDEXEES}, règle 4)")
    # aucune URL du sitemap ne doit être en noindex (le sitemap est un noyau figé : une fiche qui devient indexable
    # n'y entre pas automatiquement, elle reste indexable hors sitemap ; décision du 13/11/2026)
    for u in urls_apres:
        cle = u.replace("https://top10geek.fr/", "")
        f = "index.html" if cle == "" else (cle + "index.html" if cle.endswith("/") else cle + ".html")
        if f in noindex_apres:
            echecs.append(f"URL du sitemap en noindex : {u}")

    # 5d. lastmod : seulement pour les pages réellement changées (règle 6)
    lm_changes = [u for u in urls_apres if u in urls_avant and urls_apres[u] != urls_avant[u]]
    if urls_avant and len(lm_changes) > MAX_PART_LASTMOD * len(urls_avant):
        echecs.append(f"{len(lm_changes)} lastmod modifiés sur {len(urls_avant)} : date globale ou empreintes en cause (règle 6)")
    if len(lm_changes) > len(html_modifies):
        echecs.append(f"plus de lastmod modifiés ({len(lm_changes)}) que de pages HTML modifiées ({len(html_modifies)})")

    # 5e. Pages modifiées : H1, canonique, robots, JSON-LD
    toctoc = re.compile(r'name="robots" content="([^"]*)"')
    for f in html_modifies:
        apres = open(f, encoding="utf-8").read()
        avant = head_file(f)
        if avant is not None:
            if extrait(avant, r"<h1[^>]*>(.*?)</h1>") != extrait(apres, r"<h1[^>]*>(.*?)</h1>"):
                echecs.append(f"H1 modifié (règle 5) : {f}")
            if extrait(avant, r'rel="canonical" href="([^"]*)"') != extrait(apres, r'rel="canonical" href="([^"]*)"'):
                echecs.append(f"canonique modifiée : {f}")
            ra, rb = toctoc.search(avant), toctoc.search(apres)
            if (ra.group(1) if ra else None) != (rb.group(1) if rb else None) and f not in nouvelles_indexees:
                echecs.append(f"balise robots modifiée : {f}")
        for bloc in ld_blocs(apres):
            try:
                obj = json.loads(bloc)
            except Exception:
                echecs.append(f"JSON-LD invalide : {f}")
                continue
            for n in parcourir(obj):
                t = n.get("@type")
                types = t if isinstance(t, list) else [t]
                for interdit in ("AggregateRating", "Review", "Offer"):
                    if interdit in types:
                        echecs.append(f"{interdit} interdit (règle 11) : {f}")
                if "shippingDetails" in n or "hasMerchantReturnPolicy" in n:
                    echecs.append(f"shippingDetails / politique de retour interdits (règle 11) : {f}")
        if "utm_" in apres and (avant is None or apres.count("utm_") > avant.count("utm_")):
            echecs.append(f"paramètre de suivi « utm_ » ajouté : {f}")
        if f in ("404.html", "mentions-legales.html", "politique-confidentialite.html") and apres.count('<nav class="foot-legal"') != 1:
            echecs.append(f"navigation légale empilée : {f}")

    # 5f. Nombre de produits : ne baisse pas
    if nb_produits_avant and nb_produits and nb_produits < nb_produits_avant:
        echecs.append(f"nombre de produits en baisse ({nb_produits_avant} -> {nb_produits})")

    resume = [
        f"{len(modifs)} fichiers modifiés dont {len(html_modifies)} pages HTML",
        f"{len(lm_changes)} lastmod modifiés sur {len(urls_apres)} URL ; sitemap {len(urls_avant)} -> {len(urls_apres)} URL",
        f"{len(nouvelles_indexees)} page(s) devenues indexables ; {len(nouveaux_noindex)} passées en noindex",
        ok,
    ]
    if echecs:
        fin(3, "CONTRÔLES SEO ÉCHOUÉS : rien n'est publié", resume + [f"ÉCHEC : {e}" for e in echecs[:25]])
    fin(0, "Prêt à publier", resume)


if __name__ == "__main__":
    main()
