# -*- coding: utf-8 -*-
"""Assemble data.json (catalogue + offres marchands + notes presse) et télécharge les photos produits."""
import json, re, os, sys, subprocess, io
sys.path.insert(0, "/home/claude"); sys.path.insert(0, "/home/claude/work")
from catalog import CAT
W = "/home/claude/work/"
DATE = "02/10/2026"
ALLCC = {}
for f in ("cc_det_lap.json", "cc_det_desk.json"):
    ALLCC.update(json.load(open(W + f)))

def cckey(name):
    k = "/test-" + name + ".htm"
    if k in ALLCC: return k
    n = lambda s: s.lower().replace("++", "+").replace("+_", "_")
    for kk in ALLCC:
        if n(kk) == n(k): return kk
    raise KeyError(name)

SRCFIX = {"Clubic.com": "Clubic", "NotebookCheck": "Notebookcheck", "FrAndroid": "Frandroid", "PCWorld.com": "PCWorld", "Toms Hardware (it)": "Tom's Hardware (IT)", "Tom's Guide (US)": "Tom's Guide", "DigitalTrends": "Digital Trends", "ExpertReviews": "Expert Reviews", "RTings": "RTINGS", "PCGamer": "PC Gamer", "IndiaToday": "India Today"}

def cc_notes(p):
    out = []
    for x in ALLCC[cckey(p["name"])]:
        d = x["date"] or ""
        if d < p["since"]: continue
        blob = ((x["title"] or "") + " " + (x["url"] or "")).lower()
        if p["inc"] and not re.search(p["inc"], blob): continue
        if p["exc"] and re.search(p["exc"], blob): continue
        sc = round(x["score"] / x["max"] * 10, 2) if x["score"] is not None and x["max"] else None
        if sc is not None and sc == 0: sc = None
        out.append(dict(src=SRCFIX.get(x["src"], x["src"]), score=sc, url=x["url"], date=d))
    return out

def build_press(item):
    notes, scope, srcs = [], "modele", []
    for p in item["press"]:
        if p["kind"] == "cc":
            try: ns = cc_notes(p)
            except KeyError: print("  !! cc introuvable", p["name"]); ns = []
            if ns: srcs.append(("Synthèse CommentChoisir", "https://www.commentchoisir.fr/test-" + p["name"] + ".htm"))
        else:
            ns = [dict(src=s, score=v, url=u, date="") for s, v, u in p["notes"]]
        if p["scope"] == "gamme" and ns: scope = "gamme"
        notes += ns
    seen, uniq = set(), []
    for n in notes:
        k = (n["src"], n["url"] or n["score"])
        if k in seen: continue
        seen.add(k); uniq.append(n)
    uniq.sort(key=lambda n: (n["score"] is None, -(n["score"] or 0), n["src"]))
    scored = [n for n in uniq if n["score"] is not None]
    if not uniq: return None
    src = item.get("press_src") or (srcs[0] if srcs else (("Test " + uniq[0]["src"]), uniq[0]["url"]))
    return dict(avg=(sum(n["score"] for n in scored) / len(scored)) if scored else None, n=len(scored), tests=len(uniq), scope=scope, src=list(src), notes=uniq)

# ---------------------------------------------------------------- offres
DARTY = {x["codic"]: x for x in json.load(open(W + "darty_all.json"))}
AMZ = json.load(open(W + "amazon.json"))
GEEK = {re.search(r"geekom-(.*)/$", x["url"]).group(1): x for x in json.load(open(W + "geekom.json"))}
DARTY_MAP = {"zenbook-a14":7925166,"mba13-m5":7787766,"macbook-neo":7945833,"surface-pro-12":8015910,"surface-laptop-13":7974213,"zenbook-a16":8156573,"omnibook5-14":8265291,"ideapad-slim3x":8167109,"galaxy-book4-edge":8096538,"vivobook-s14":8159009,"mbp14-m5":7945728,"proart-p16":8315183,"proart-px13":8315230,"yoga-pro9":8175470,"yoga-pro7":8193940,"zenbook-duo":8213895,"aero-x16":8190739,"mba15-m5":7945523,"zephyrus-g16":8200106,"omen-max-16":7997299,"legion5":8175667,"loq15":8140464,"katana15":8006946,"cyborg15":8033544,"crosshair16":7920857,"strix-g16":8039160,"gigabyte-a16":8040672,"nitro-v16":7996918,"yoga-slim7":8305099,"yoga-slim7x":8235015,"zenbook-s14":8315213,"zenbook-s16":8213917,"omnibook-x-flip14":8321817,"yoga7-2in1":8193860,"ideapad-slim5-16":8193983,"swift16ai":8174300,"lg-gram17":8307750,"aspire-go-15":8033188,"ideapad1":7728883,"chromebook-315":8174245,"chromebook-plus-514":8174318,"chromebook-duet":8048037,"vivobook-14":8156522,"vivobook-go-14":8289026,"lenovo-v15":8212457,"chromebook-cx14":8209766,"ideapad-slim3":8286264,
"mac-mini-m6":7788037,"mac-mini-m5pro":7787987,"mac-studio-m5max":7787871,"imac-m4":7055200,"ideacentre-mini":8187738,"omnidesk-slim":8163634,"dell-slim":8155100,"ideacentre-tower":8175632,"asus-v500":8158630,"omen35l":8037035,"omen16l":8037043,"loq-tower":8175551,"nitro-50":8009600,"rog-g700":8158614,"aorus-prime-5":8287090,"omnistudio-x32":7946767,"omnistudio-x27":8319995,"hp-omnistudio-27":8331480,"yoga-aio-32":8268142,"ideacentre-aio-27":8175608,"asus-v400":8157901,"msi-modern-am273":7937075}
AMZ_MAP = {"geekom-air12-lite":"geekom-air12-lite","beelink-ser9pro":"beelink-ser9pro","nipogi-am06pro":"nipogi-am06pro","gmktec-k13":"gmktec-k13","hp-z2-mini":"hp-z2-mini","thinkstation-p3":"thinkstation-p3","legion-tower-5":"legion-tower-5","nitro-60":"nitro-60","area-51":"area-51","dell-24-aio":"dell-24-aio"}
AMZ_SKIP = set()
GEEK_MAP = {"geekom-a5":"a5-mini-pc","geekom-a5pro":"a5-pro-mini-pc-2026-edition","geekom-a6":"a6-mini-pc","geekom-a7":"a7-mini-pc","geekom-a8":"a8-mini-pc","geekom-a9max":"a9-max-mini-pc","geekom-gt1mega":"gt1-mega-mini-pc","geekom-it13":"it13-mini-pc","geekom-it12":"mini-it12-mini-pc","geekom-air12-lite":"mini-air-12-lite-mini-pc","geekom-it15":"mini-it15-mini-pc"}
AS = "https://static2-ecemea.acer.com/media/catalog/product/"
ACER = {
 "aspire-go-15": dict(price=749.99, url="https://store.acer.com/fr-fr/acer-aspire-go-15-ordinateur-portable-ag15-42p-argent-nx-j7wef-00g", name="Acer Aspire Go 15 AG15-42P (NX.J7WEF.00G)", img=None),
 "swift-air-14": dict(price=899.99, url="https://store.acer.com/fr-fr/acer-swift-air-14-ordinateur-portable-ultrafin-sfa14-i31-rose", name="Acer Swift Air 14 SFA14-I31 Rose (NX.W4BEF.001)", img=AS + "a/c/acer-swift-air-14-sfa14-i31-non-fingerprint-with-backlit-on-wp-copilot-blossom-pink-01_5.jpg"),
 "orion-7000": dict(price=2499.99, url="https://store.acer.com/fr-fr/predator-orion-7000-pc-gamer-po7-655-noir-dg-e3zef-019", name="Predator Orion 7000 PO7-655 · Core i7-14700KF · 32 Go · 1 To SSD · RTX 4080 SUPER", img=AS + "p/r/predator-orion-7000-po7-655-light-rgb-usbkm-rgb-01.jpg"),
 "aspire-xc": dict(price=799.99, url="https://store.acer.com/fr-fr/acer-aspire-xc-pc-de-bureau-xc-1860-noir-dt-bmyeh-005", name="Acer Aspire XC-1860 · Core Ultra 5 225 · 8 Go · 512 Go SSD", img=AS + "a/c/acer-aspire-xc-1860-non-odd-with-sd-card-reader-02_1.jpg"),
 "aspire-c27": dict(price=1099.99, url="https://store.acer.com/fr-fr/acer-aspire-c-27-b-ai-tout-en-un-c27b-gkrk-noir", name="Acer Aspire C 27-B AI C27B-GKRK · Ryzen 5 330 · 8 Go · 512 Go SSD", img=AS + "a/c/acer-aspire-c27-ai-c27b-gkrk-c27b-gstx-wp-black-01-1_5.jpg"),
}

def cfg(name):
    """Résumé court de la configuration à partir du libellé marchand (RAM · stockage · carte graphique)."""
    n = name.replace("\u00a0", " ")
    toks = []
    for m in re.finditer(r"(\d{1,4})\s?(Go|GB|To|TB|to|go|Gb|G)\b(?=(.{0,14}))", n):
        v, u, after = int(m.group(1)), m.group(2).lower(), m.group(3)
        if re.match(r"\s?(GDDR|VRAM|de mémoire dédiée|dédié)", after) or re.search(r"(RTX|GTX|RX|Radeon|GeForce)[^,|/()-]{0,22}$", n[:m.start()]):
            continue
        toks.append((v, "To" if u in ("to", "tb") else "Go", m.start()))
    ram = next((t for t in toks if t[1] == "Go" and t[0] in (4, 8, 12, 16, 24, 32, 36, 48, 64, 96, 128)), None)
    sto = next((t for t in toks if t is not ram and (t[1] == "To" or t[0] >= 64)), None)
    out = []
    if ram: out.append(f"{ram[0]} Go")
    if sto:
        v, u = sto[0], sto[1]
        if u == "Go" and v >= 1000: v, u = v // 1000, "To"
        out.append(f"{v} {u}")
    g = re.search(r"(RTX|RX)\s?(\d{4})\s?(Ti|SUPER|Super|XT)?", n)
    if g: out.append((g.group(1) + " " + g.group(2) + (" " + g.group(3).replace("Super", "SUPER") if g.group(3) else "")))
    return " · ".join(out)

AMAZON_TAG = ""   # identifiant Partenaires Amazon (ex. top10geek-21) : à renseigner, il sera ajouté à tous les liens Amazon

def offers(pid):
    out, imgs = [], []
    if pid in DARTY_MAP:
        x = DARTY[str(DARTY_MAP[pid])]
        nm = (x["brand"] + " " + x["ref"]).strip()
        out.append(dict(m="Darty", price=float(x["price"]), url=x["url"].split("#")[0], name=nm, cfg=cfg(nm)))
        mm = re.search(r"source=([^&]+)", x.get("img") or "")
        if mm and "/market/" in mm.group(1):
            imgs.append("https://image.darty.com/darty?type=image&source=" + mm.group(1) + "&width=640&height=480&quality=92")
        item_r = (x.get("rating"), x.get("nrev"))
    else:
        item_r = (None, 0)
    if pid in GEEK_MAP:
        g = GEEK[GEEK_MAP[pid]]
        out.append(dict(m="Geekom", price=min(float(p) for p in g["prices"]), url=g["url"], name=g["title"], cfg=""))
        if g.get("img"): imgs.append(g["img"])
    if pid in ACER:
        a = ACER[pid]
        out.append(dict(m="Acer Store", price=a["price"], url=a["url"], name=a["name"], cfg=cfg(a["name"])))
        if a["img"]: imgs.append(a["img"])
    k = AMZ_MAP.get(pid, pid)
    if k in AMZ and pid not in AMZ_SKIP and AMZ[k]["price"]:
        a = AMZ[k]
        url = "https://www.amazon.fr/dp/" + a["asin"] + ("?tag=" + AMAZON_TAG if AMAZON_TAG else "")
        out.append(dict(m="Amazon", price=a["price"], url=url, name=a["name"], cfg=cfg(a["name"]), asin=a["asin"]))
        imgs.append(a["img"])
    return out, imgs, item_r

def fetch_img(urls, dest):
    from PIL import Image
    if os.path.exists(dest): return True
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36"
    for u in urls:
        r = subprocess.run(["curl", "-sS", "-m", "30", "-L", "-A", UA, u], capture_output=True)
        try:
            im = Image.open(io.BytesIO(r.stdout)).convert("RGBA")
        except Exception as e:
            print("  img KO", u[:80], e); continue
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im); im = bg.convert("RGB")
        # rognage des marges blanches puis cadre 4:3 sur fond blanc
        from PIL import ImageChops
        diff = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).convert("L").point(lambda v: 255 if v > 14 else 0)
        box = diff.getbbox()
        if box: im = im.crop(box)
        Wd, Hd = 560, 420
        im.thumbnail((Wd - 36, Hd - 36), Image.LANCZOS)
        canvas = Image.new("RGB", (Wd, Hd), (255, 255, 255))
        canvas.paste(im, ((Wd - im.width) // 2, (Hd - im.height) // 2))
        canvas.save(dest, "WEBP", quality=82, method=6)
        return True
    return False

# photos : par défaut Darty > Geekom > Acer > Amazon ; exceptions quand le visuel Darty est un carton de pack ou un visuel manquant
IMG_AMAZON_FIRST = {"zenbook-a16", "surface-pro-12", "chromebook-315", "mac-mini-m6", "mac-mini-m5pro"}
IMG_EXTRA = {}

if __name__ == "__main__":
    IMG = "/home/claude/img_p"; os.makedirs(IMG, exist_ok=True)
    data = {}
    for pid, it in CAT.items():
        offs, imgs, (rt, nrev) = offers(pid)
        assert offs, "aucune offre : " + pid
        pr = build_press(it)
        assert pr, "aucun test presse : " + pid
        if pid in IMG_AMAZON_FIRST: imgs = imgs[::-1]
        if pid in IMG_EXTRA: imgs = IMG_EXTRA[pid] + imgs
        ok = fetch_img(imgs, f"{IMG}/{pid}.webp")
        d = {k: v for k, v in it.items() if k not in ("press", "press_src")}
        d.update(id=pid, press=pr, offers=sorted(offs, key=lambda o: o["price"]), img=(pid + ".webp") if ok else None, rating=rt, nrev=nrev or 0, m=list(it["m"]))
        data[pid] = d
    json.dump(dict(date=DATE, items=data), open("/home/claude/data.json", "w"), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(data), Counter(d["cat"] for d in data.values()))
    for pid, d in data.items():
        p = d["press"]
        print(f"{pid:22s} {d['cat']:11s} {('%.1f' % p['avg']) if p['avg'] else ' — '} n={p['n']:2d}/{p['tests']:2d} {p['scope'][:3]} | " + " ; ".join(f"{o['m']} {o['price']:.0f} [{o['cfg']}]" for o in d["offers"]) + ("" if d["img"] else "  !! SANS PHOTO"))
