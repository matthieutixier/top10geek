// Mesure des clics vers les marchands (décision du 20/10/2026).
// Le site envoie un signal (navigator.sendBeacon, assets/main.js) au moment du clic ; le lien marchand reste un lien direct
// (pas de redirection : rien ne change pour Amazon ni pour le suivi Effinity).
// Stockage : base Cloudflare D1 liée au projet Pages sous le nom « DB » (Réglages > Liaisons). Sans liaison, la fonction ne fait rien.
// Aucune donnée personnelle : ni cookie, ni adresse IP, ni identifiant.
// Colonne « source » (29/10/2026) : canal d'arrivée (pinterest, reddit, linkedin...), vide si inconnu ; m = 'arrivee' = une arrivée par session avec source.
// Lecture : console D1 du tableau de bord Cloudflare, par exemple
//   SELECT page, marchand, zone, COUNT(*) n FROM clics WHERE ts >= date('now','-30 day') GROUP BY 1,2,3 ORDER BY n DESC;

const ORIGINES = /^https:\/\/((www\.)?top10geek\.fr|([a-z0-9-]+\.)?top10geek\.pages\.dev)$/;
let tablePrete = false;

export async function onRequestPost({ request, env }) {
  const vide = new Response(null, { status: 204 });
  try {
    if (!env.DB) return vide;
    let origine = request.headers.get("Origin") || "";
    if (!origine) {
      try { origine = new URL(request.headers.get("Referer") || "").origin; } catch (e) { origine = ""; }
    }
    if (!ORIGINES.test(origine)) return vide;
    const texte = await request.text();
    if (texte.length > 1000) return vide;
    const d = JSON.parse(texte);
    const s = (v, n) => String(v ?? "").slice(0, n);
    if (!tablePrete) {
      await env.DB.prepare(
        "CREATE TABLE IF NOT EXISTS clics (ts TEXT NOT NULL, page TEXT, marchand TEXT, produit TEXT, zone TEXT, appareil TEXT)"
      ).run();
      try { await env.DB.prepare("ALTER TABLE clics ADD COLUMN source TEXT").run(); } catch (e) { /* colonne déjà présente */ }
      tablePrete = true;
    }
    const src = /^[a-z0-9_-]{1,20}$/i.test(String(d.s ?? "")) ? String(d.s).toLowerCase() : "";   // canal de la visite (utm_source), sinon vide
    await env.DB.prepare("INSERT INTO clics (ts, page, marchand, produit, zone, appareil, source) VALUES (datetime('now'), ?, ?, ?, ?, ?, ?)")
      .bind(s(d.p, 200), s(d.m, 40), s(d.id, 80), s(d.z, 30), s(d.a, 10), src)
      .run();
  } catch (e) {
    // une mesure perdue ne doit jamais gêner le visiteur
  }
  return vide;
}

export function onRequest() {
  return new Response(null, { status: 405, headers: { Allow: "POST" } });
}
