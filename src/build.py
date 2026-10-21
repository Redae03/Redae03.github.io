"""Génère le site du portfolio à partir de src/content.json.

Usage (depuis la racine du dépôt) :
    python src/build.py

Pour ajouter un stage, un projet, un certificat ou une activité, il suffit de compléter
src/content.json puis de relancer ce script. Les simulateurs sont dans src/sim/<slug>.html.
"""
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
C = json.loads((SRC / "content.json").read_text(encoding="utf-8"))
SITE = C["site"]
SIM_SLUGS = json.loads((SRC / "sim" / "_slugs.json").read_text(encoding="utf-8"))

UI = {
    "fr": {
        "nav": [("phares", "Projets phares"), ("experience", "Expérience"), ("projets", "Projets"), ("formation", "Formation"), ("activites", "Activités"), ("contact", "Contact")],
        "flagships": "Projets phares", "flagships_side": "Trois études de cas complètes, avec données, méthode, résultats chiffrés et limites.",
        "experience": "Expérience", "experience_side": "Stages réalisés pendant le cycle ingénieur.",
        "projects": "Autres projets", "projects_side": "Chaque projet est publié avec son code, son rapport et un simulateur.",
        "education": "Formation", "certs": "Certifications", "certs_note": "Cliquez sur un certificat pour le vérifier sur le site de l’organisme.",
        "skills": "Compétences", "activities": "Activités", "contact": "Contact",
        "contact_text": "Pour échanger sur l’un de ces projets, écrivez-moi.",
        "copy": "Copier l’adresse", "copied": "Adresse copiée",
        "case": "Lire l’étude de cas", "sim": "Simuler", "code": "Code", "code_report": "Code et rapport", "report": "Rapport (PDF)",
        "contact_btn": "Me contacter", "updated": "Mis à jour en octobre 2026",
        "problem": "Question", "method": "Méthode", "results": "Résultats", "limits": "Limites et suites",
        "back": "← Retour au portfolio", "other_cases": "Autres études de cas", "lang_other": "English", "sim_bar": "Simulateur interactif",
        "sim_label": "Simuler", "proj_head": ["Projet", "Méthodes", "Année"],
        "desc": "Portfolio de Reda Erraoui, élève ingénieur en finance quantitative : risque de marché, produits dérivés et économétrie financière en Python. Projets, simulateurs interactifs et certificats vérifiables.",
        "months": ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."],
    },
    "en": {
        "nav": [("phares", "Featured work"), ("experience", "Experience"), ("projets", "Projects"), ("formation", "Education"), ("activites", "Activities"), ("contact", "Contact")],
        "flagships": "Featured work", "flagships_side": "Three complete case studies with data, method, quantified results and limitations.",
        "experience": "Experience", "experience_side": "Internships completed during the engineering program.",
        "projects": "Other projects", "projects_side": "Each project is published with its code, report and a simulator.",
        "education": "Education", "certs": "Certifications", "certs_note": "Click a certificate to verify it on the issuer’s website.",
        "skills": "Skills", "activities": "Activities", "contact": "Contact",
        "contact_text": "To discuss any of these projects, get in touch.",
        "copy": "Copy address", "copied": "Address copied",
        "case": "Read the case study", "sim": "Simulator (French interface)", "code": "Code", "code_report": "Code and report", "report": "Report (PDF, French)",
        "contact_btn": "Get in touch", "updated": "Updated October 2026",
        "problem": "Question", "method": "Method", "results": "Results", "limits": "Limitations and next steps",
        "back": "← Back to portfolio", "other_cases": "Other case studies", "lang_other": "Français", "sim_bar": "Interactive simulator",
        "sim_label": "Simulator", "proj_head": ["Project", "Methods", "Year"],
        "desc": "Portfolio of Reda Erraoui, engineering student in quantitative finance: market risk, derivatives pricing and financial econometrics in Python. Projects, interactive simulators and verifiable certificates.",
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    },
}

esc = html.escape


def t(v, lang):
    return v[lang] if isinstance(v, dict) else v


def gh(repo, path=""):
    return f"{SITE['github']}/{repo}" + (f"/blob/main/{path}" if path else "")


def head(lang, title, desc, rel, path_fr, path_en, og):
    """En-tête commun. rel : préfixe relatif vers la racine ('', '../', '../../')."""
    url = SITE["url"]
    ga = SITE.get("analytics_goatcounter") or ""
    analytics = (f'<script data-goatcounter="https://{ga}.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>\n' if ga else "")
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Reda Erraoui">
<meta name="theme-color" content="#0f2a4a">
<link rel="canonical" href="{url}/{path_fr if lang == 'fr' else path_en}">
<link rel="alternate" hreflang="fr" href="{url}/{path_fr}">
<link rel="alternate" hreflang="en" href="{url}/{path_en}">
<link rel="alternate" hreflang="x-default" href="{url}/{path_en}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}/{path_fr if lang == 'fr' else path_en}">
<meta property="og:image" content="{url}/assets/{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{'fr_FR' if lang == 'fr' else 'en_US'}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Source+Sans+3:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{rel}assets/css/site.css">
{analytics}</head>
"""


def topbar(lang, rel, other_href, nav=True, home=None):
    u = UI[lang]
    home = home or (f"{rel}index.html" if lang == "fr" else f"{rel}en/index.html")
    links = "".join(f'<a href="#{i}">{l}</a>' for i, l in u["nav"]) if nav else ""
    return f"""<div class="topbar">
  <div class="wrap">
    <a class="mark" href="{home}">Reda Erraoui</a>
    <nav class="topnav" aria-label="{'Sections' if lang == 'fr' else 'Sections'}">{links}</nav>
    <a class="lang" href="{other_href}" hreflang="{'en' if lang == 'fr' else 'fr'}" lang="{'en' if lang == 'fr' else 'fr'}">{u['lang_other']}</a>
  </div>
</div>
"""


def cert_date(d, lang):
    y, m = d.split("-")
    return f"{UI[lang]['months'][int(m) - 1].capitalize()} {y}"


def link_row(lang, rel, case=None, sim=None, repo=None, report=False, case_first=True):
    u = UI[lang]
    out = []
    if case:
        out.append(f'<a class="cta" href="{rel}{"projets" if lang == "fr" else "en/projects"}/{case}.html">{u["case"]} →</a>')
    if sim:
        out.append(f'<a class="simlink" href="{rel}simulateurs/{sim}.html">{u["sim_label"]}</a>')
    if repo:
        out.append(f'<a href="{gh(repo)}" target="_blank" rel="noopener">{u["code_report"] if report else u["code"]}</a>')
    return '<p class="links-row">' + " ".join(out) + "</p>" if out else ""


def footer(lang):
    return f"""<footer><div class="wrap"><span>Reda Erraoui · {UI[lang]['updated']}</span><span><a href="{SITE['linkedin']}" target="_blank" rel="noopener">LinkedIn</a> · <a href="{SITE['github']}" target="_blank" rel="noopener">GitHub</a></span></div></footer>
"""


def index_page(lang):
    u = UI[lang]
    rel = "" if lang == "fr" else "../"
    H = C["hero"]
    other = "en/index.html" if lang == "fr" else "../index.html"
    title = "Reda Erraoui · " + ("Finance quantitative" if lang == "fr" else "Quantitative finance")
    p = [head(lang, title, u["desc"], rel, "", "en/", f"og-{lang}.png"), "<body>\n", topbar(lang, rel, other)]
    details = "".join(f"<dt>{t(d['k'], lang)}</dt><dd>{t(d['v'], lang)}</dd>" for d in H["details"])
    p.append(f"""<header class="intro" id="top">
  <div class="wrap">
    <div>
      <div class="small-caps">{t(H['eyebrow'], lang)}</div>
      <h1>Reda Erraoui</h1>
      <p class="title">{t(H['positioning'], lang)}</p>
      <p class="summary">{t(H['summary'], lang)}</p>
      {f'<dl class="details">{details}</dl>' if details else ""}
      <div class="actions">
        <a class="btn solid" href="#contact">{u['contact_btn']}</a>
        <a class="btn line" href="{SITE['linkedin']}" target="_blank" rel="noopener">LinkedIn</a>
        <a class="btn line" href="{SITE['github']}" target="_blank" rel="noopener">GitHub</a>
      </div>
    </div>
    <figure class="portrait"><img src="{rel}assets/img/portrait-420.webp" width="420" height="510" alt="{'Portrait de Reda Erraoui' if lang == 'fr' else 'Portrait of Reda Erraoui'}" fetchpriority="high"></figure>
  </div>
</header>
<div class="keys"><div class="wrap">""")
    for k in C["keys"]:
        p.append(f"<div><b>{t(k['n'], lang)}</b><span>{t(k['t'], lang)}</span></div>")
    p.append("</div></div>\n<main>\n")

    # Projets phares
    p.append(f'<section id="phares"><div class="wrap sec"><div class="side"><h2>{u["flagships"]}</h2><p>{u["flagships_side"]}</p></div><div class="cards">')
    for f in C["flagships"]:
        p.append(f"""<article class="card">
  <div class="small-caps">{t(f['theme'], lang)}</div>
  <h3><a href="{rel}{'projets' if lang == 'fr' else 'en/projects'}/{f['slug']}.html">{t(f['title'], lang)}</a></h3>
  <p class="ctx">{t(f['context'], lang)}</p>
  <p>{t(f['hook'], lang)}</p>
  {link_row(lang, rel, f['slug'], f['sim'], f['repo'])}
</article>""")
    p.append("</div></div></section>\n")

    # Expérience
    p.append(f'<section id="experience"><div class="wrap sec"><div class="side"><h2>{u["experience"]}</h2><p>{u["experience_side"]}</p></div><div>')
    for e in C["experience"]:
        lis = "".join(f"<li>{b}</li>" for b in t(e["bullets"], lang))
        p.append(f"""<article class="entry">
  <div class="when"><b>{t(e['when'], lang)}</b>{t(e['meta'], lang)}</div>
  <div>
    <h3>{t(e['title'], lang)}</h3>
    <div class="org">{t(e['org'], lang)}</div>
    <ul>{lis}</ul>
    <div class="stack"><b>{'Outils' if lang == 'fr' else 'Tools'} :</b> {t(e['tools'], lang)}</div>
    {link_row(lang, rel, e.get('case'), e.get('sim'), e.get('repo'), report=True)}
  </div>
</article>""".replace("<b>Tools :</b>", "<b>Tools:</b>"))
    p.append("</div></div></section>\n")

    # Autres projets
    hd = u["proj_head"]
    p.append(f'<section id="projets"><div class="wrap sec"><div class="side"><h2>{u["projects"]}</h2><p>{u["projects_side"]}</p></div><div class="projects"><div class="thead small-caps"><span>{hd[0]}</span><span>{hd[1]}</span><span>{hd[2]}</span></div>')
    for pr in C["projects"]:
        p.append(f"""<div class="proj"><div><h3>{t(pr['title'], lang)}</h3><p>{t(pr['text'], lang)}</p>{link_row(lang, rel, None, pr.get('sim'), pr.get('repo'))}</div><div class="meth">{pr['meth']}</div><div class="yr">{pr['year']}</div></div>""")
    p.append("</div></div></section>\n")

    # Formation et certifications
    E = C["education"]
    certs = []
    for grp in C["certifications"]:
        items = "".join(f'<li><a href="{url}" target="_blank" rel="noopener">{esc(n)}</a><span>{cert_date(d, lang)}</span></li>' for n, url, d in grp["items"])
        certs.append(f'<div class="org">{grp["org"]}</div><ul class="certs">{items}</ul>')
    p.append(f"""<section id="formation"><div class="wrap sec"><div class="side"><h2>{u['education']}</h2></div><div class="cols">
  <div><h3>{t(E['school'], lang)}</h3><p class="org">{t(E['degree'], lang)}</p><p>{t(E['courses'], lang)}</p><p class="muted">{t(E['bac'], lang)}</p></div>
  <div><h3>{u['certs']}</h3>{''.join(certs)}<p class="certs-note">{u['certs_note']}</p></div>
</div></div></section>
""")

    # Compétences
    p.append(f'<section id="competences"><div class="wrap sec"><div class="side"><h2>{u["skills"]}</h2></div><div class="skills">')
    for s in C["skills"]:
        p.append(f"<div><h3>{t(s['h'], lang)}</h3><ul>" + "".join(f"<li>{i}</li>" for i in t(s["items"], lang)) + "</ul></div>")
    p.append("</div></div></section>\n")

    # Activités
    p.append(f'<section id="activites"><div class="wrap sec"><div class="side"><h2>{u["activities"]}</h2></div><div>')
    for a in C["activities"]:
        figs = []
        for j, (src, w, hgt, alt) in enumerate(a["imgs"]):
            cls = ' class="tall"' if a["gallery"] == "triple" and j == 0 else ""
            cap = f"<figcaption>{t(a['caption'], lang)}</figcaption>" if j == len(a["imgs"]) - 1 else ""
            figs.append(f'<figure{cls}><img src="{rel}assets/img/{src}" width="{w}" height="{hgt}" alt="{esc(t(alt, lang))}" loading="lazy" decoding="async">{cap}</figure>')
        gcls = {"pair": "gallery", "triple": "gallery3", "masonry": "gallery-m"}[a["gallery"]]
        p.append(f"""<article class="event"><div class="event-head"><h3>{t(a['title'], lang)}</h3><span>{t(a['meta'], lang)}</span></div><p>{t(a['text'], lang)}</p><div class="{gcls}">{''.join(figs)}</div></article>""")
    p.append("</div></div></section>\n")

    # Contact
    p.append(f"""<section class="contact" id="contact"><div class="wrap sec"><div class="side"><h2>{u['contact']}</h2></div><div class="contact-body">
  <p>{u['contact_text']}</p>
  <div class="mailrow"><span class="mail" id="mail">{SITE['email']}</span><button type="button" class="copy" id="copy">{u['copy']}</button></div>
  <p class="links"><a href="{SITE['linkedin']}" target="_blank" rel="noopener">LinkedIn</a> · <a href="{SITE['github']}" target="_blank" rel="noopener">GitHub</a></p>
</div></div></section>
</main>
""")
    p.append(footer(lang))
    legacy = json.dumps(SIM_SLUGS)
    p.append(f"""<script>
(function () {{
  var copy = document.getElementById("copy"), mail = document.getElementById("mail");
  copy.addEventListener("click", function () {{
    var ok = function () {{ copy.textContent = "{u['copied']}"; setTimeout(function () {{ copy.textContent = "{u['copy']}"; }}, 1800); }};
    var fb = function () {{ var r = document.createRange(); r.selectNodeContents(mail); var s = getSelection(); s.removeAllRanges(); s.addRange(r); }};
    try {{ navigator.clipboard.writeText(mail.textContent).then(ok, fb); }} catch (e) {{ fb(); }}
  }});
  // Anciens liens (#simulateur-…) : redirection vers la page du simulateur
  var legacy = {legacy}, h = location.hash.slice(1);
  if (legacy[h]) location.replace("{rel}simulateurs/" + legacy[h] + ".html");
}})();
</script>
</body>
</html>
""")
    return "".join(p)


def case_page(f, lang):
    u = UI[lang]
    rel = "../" if lang == "fr" else "../../"
    path_fr, path_en = f"projets/{f['slug']}.html", f"en/projects/{f['slug']}.html"
    other = (f"../en/projects/{f['slug']}.html" if lang == "fr" else f"../../projets/{f['slug']}.html")
    home = f"{rel}index.html" if lang == "fr" else f"{rel}en/index.html"
    title = f"{t(f['title'], lang)} · Reda Erraoui"
    R = f["results"]
    rows = R["rows"] if lang == "fr" else R["rows_en"]
    thead = "".join(f"<th>{h}</th>" for h in t(R["head"], lang))
    tbody = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    meth = "".join(f"<li>{m}</li>" for m in t(f["method"], lang))
    lim = "".join(f"<li>{m}</li>" for m in t(f["limits"], lang))
    others = "".join(f'<li><a href="{o["slug"]}.html">{t(o["title"], lang)}</a></li>' for o in C["flagships"] if o["slug"] != f["slug"])
    related = (f'<p class="muted">{t(f["related"], lang)} <a href="{home}#projets">{"Voir les autres projets" if lang == "fr" else "See other projects"} →</a></p>' if t(f["related"], lang) else "")
    return f"""{head(lang, title, t(f['hook'], lang), rel, path_fr, path_en, f'og-{lang}.png')}<body>
{topbar(lang, rel, other, nav=False, home=home)}<header class="case-head"><div class="wrap">
  <a class="back" href="{home}#phares">{u['back']}</a>
  <div class="small-caps">{t(f['theme'], lang)}</div>
  <h1>{t(f['title'], lang)}</h1>
  <p class="ctx">{t(f['context'], lang)}</p>
  <p class="hook">{t(f['hook'], lang)}</p>
  <div class="actions">
    <a class="btn solid" href="{rel}simulateurs/{f['sim']}.html">{u['sim']}</a>
    <a class="btn line" href="{gh(f['repo'])}" target="_blank" rel="noopener">{u['code']} (GitHub)</a>
    <a class="btn line" href="{gh(f['repo'], f['report'])}" target="_blank" rel="noopener">{u['report']}</a>
  </div>
</div></header>
<main class="case">
<section><div class="wrap sec"><div class="side"><h2>{u['problem']}</h2></div><div><p class="lead">{t(f['problem'], lang)}</p></div></div></section>
<section><div class="wrap sec"><div class="side"><h2>{u['method']}</h2></div><div><ol class="steps">{meth}</ol></div></div></section>
<section><div class="wrap sec"><div class="side"><h2>{u['results']}</h2></div><div><div class="tbl-wrap"><table class="res case-table"><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div><p class="note">{t(R['note'], lang)}</p></div></div></section>
<section><div class="wrap sec"><div class="side"><h2>{u['limits']}</h2></div><div><ul class="steps">{lim}</ul>{related}</div></div></section>
<section><div class="wrap sec"><div class="side"><h2>{u['other_cases']}</h2></div><div><ul class="plainlinks">{others}</ul></div></div></section>
</main>
{footer(lang)}</body>
</html>
"""


def sim_page(slug, body):
    rel = "../"
    names = {v: k for k, v in SIM_SLUGS.items()}
    title = "Simulateur · Reda Erraoui"
    return f"""{head('fr', title, UI['fr']['desc'], rel, f'simulateurs/{slug}.html', f'simulateurs/{slug}.html', 'og-fr.png')}<body class="simpage-body">
<div class="simbar"><div class="wrap"><a class="simback" href="../index.html">{UI['fr']['back']}</a><span class="small-caps">{UI['fr']['sim_bar']}</span><a class="lang" href="../en/index.html" lang="en">English site</a></div></div>
<main>
{body}
</main>
{footer('fr')}<script>
(function () {{
  // Retour : revient à la page précédente du portfolio si on en vient, sinon à l'accueil
  var b = document.querySelector(".simback");
  if (document.referrer && document.referrer.indexOf(location.host) >= 0) b.addEventListener("click", function (e) {{ e.preventDefault(); history.back(); }});
}})();
</script>
</body>
</html>
"""


def main():
    out = ROOT
    (out / "assets" / "css").mkdir(parents=True, exist_ok=True)
    base = (SRC / "base.css").read_text(encoding="utf-8")
    extra = (SRC / "extra.css").read_text(encoding="utf-8")
    (out / "assets" / "css" / "site.css").write_text(base + "\n" + extra, encoding="utf-8")
    (out / "index.html").write_text(index_page("fr"), encoding="utf-8")
    (out / "en").mkdir(exist_ok=True)
    (out / "en" / "index.html").write_text(index_page("en"), encoding="utf-8")
    (out / "projets").mkdir(exist_ok=True)
    (out / "en" / "projects").mkdir(parents=True, exist_ok=True)
    for f in C["flagships"]:
        (out / "projets" / f"{f['slug']}.html").write_text(case_page(f, "fr"), encoding="utf-8")
        (out / "en" / "projects" / f"{f['slug']}.html").write_text(case_page(f, "en"), encoding="utf-8")
    (out / "simulateurs").mkdir(exist_ok=True)
    for slug in SIM_SLUGS.values():
        body = (SRC / "sim" / f"{slug}.html").read_text(encoding="utf-8")
        (out / "simulateurs" / f"{slug}.html").write_text(sim_page(slug, body), encoding="utf-8")
    pages = ["", "en/"] + [f"projets/{f['slug']}.html" for f in C["flagships"]] + [f"en/projects/{f['slug']}.html" for f in C["flagships"]] + [f"simulateurs/{s}.html" for s in SIM_SLUGS.values()]
    sm = "".join(f"<url><loc>{SITE['url']}/{p}</loc></url>" for p in pages)
    (out / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n', encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n", encoding="utf-8")
    print("Site généré :", len(pages), "pages")


if __name__ == "__main__":
    main()
