# redaerraoui.github.io

Portfolio de Reda Erraoui : [redaerraoui.github.io](https://redaerraoui.github.io) (version anglaise : [/en/](https://redaerraoui.github.io/en/)).

## Structure

| Dossier | Contenu |
|---|---|
| `src/content.json` | **Tout le texte du site**, en français et en anglais : stages, projets phares, autres projets, formation, certificats, compétences, activités |
| `src/build.py` | Génère les pages à partir de `content.json` |
| `src/sim/` | Un fichier par simulateur interactif |
| `src/base.css`, `src/extra.css` | Style du site |
| `index.html`, `en/`, `projets/`, `simulateurs/` | Pages générées (ne pas modifier à la main) |
| `assets/` | Feuille de style générée, images, icône, aperçus pour LinkedIn |

## Ajouter quelque chose

1. Ouvrir `src/content.json` et ajouter un élément dans la bonne liste, en copiant un élément existant :
   - un stage : `experience` (en tête de liste pour le plus récent) ;
   - un projet : `projects`, ou `flagships` pour une étude de cas complète ;
   - un certificat : `certifications` (nom, lien de vérification, date `AAAA-MM`) ;
   - une activité : `activities`, avec ses photos dans `assets/img/`.
2. Lancer `python src/build.py` depuis la racine du dépôt.
3. Vérifier en local avec `python -m http.server`, puis ouvrir http://localhost:8000.
4. Faire un commit et un push : GitHub Pages met le site à jour en une à deux minutes.

Chaque texte existe en deux versions, `"fr"` et `"en"`.

## Statistiques de visite (facultatif)

Créer un compte gratuit sur [GoatCounter](https://www.goatcounter.com), puis indiquer le code choisi dans `site.analytics_goatcounter` de `content.json` et relancer `python src/build.py`. GoatCounter ne dépose pas de cookies.
