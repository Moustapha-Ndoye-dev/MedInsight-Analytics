from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter
import nbformat
import os
from bs4 import BeautifulSoup, Comment
import asyncio
import platform


# ──────────────────────────────────────────────────────────────────────────────
# Suppression des commentaires HTML
# ──────────────────────────────────────────────────────────────────────────────
def remove_html_comments(html_content):
    """Supprime tous les commentaires HTML du contenu."""
    soup = BeautifulSoup(html_content, "html.parser")
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    return str(soup)


# ──────────────────────────────────────────────────────────────────────────────
# Transformation du DOM + injection CSS premium
# ──────────────────────────────────────────────────────────────────────────────
def apply_premium_design(html_content):
    """
    Restructure le DOM du notebook converti et injecte un design premium
    orienté rapport d'intelligence hospitalière.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # ── 1. Harmonisation des divs inline du notebook (bandeaux dégradés, etc.) ──
    for div in soup.find_all("div", style=True):
        st = div.get("style", "").lower()
        # Remplacer les dégradés bleu marine par le teal santé
        if "linear-gradient" in st and any(c in st for c in ["1e3c", "2a52", "1565", "0d47"]):
            div["style"] = (
                "background: linear-gradient(135deg, #0d9488 0%, #065f46 100%);"
                "padding: 48px 60px; border-radius: 20px;"
                "box-shadow: 0 20px 60px rgba(6,95,70,0.25);"
                "text-align: center; color: white !important; margin: 0 0 48px 0;"
                "position: relative; overflow: hidden;"
            )
            for tag in div.find_all(["h1", "h2", "h3", "h4", "p", "em", "strong", "span", "li"]):
                existing = tag.get("style", "")
                tag["style"] = existing + "; color: white !important; border: none !important; text-shadow: 0 2px 4px rgba(0,0,0,0.3);"
        # Corriger les bordures latérales colorées
        if "border-left" in st:
            for old, new in [("#2ecc71", "#0d9488"), ("#1e3c72", "#0d9488"), ("#f8fbfa", "#ecfdf5"), ("#27ae60", "#059669")]:
                div["style"] = div["style"].replace(old, new)

    # ── 1b. Force le texte blanc sur TOUS les divs à fond sombre/coloré ──
    DARK_BG_KEYWORDS = [
        "linear-gradient", "#0d9488", "#065f46", "#047857", "#064e3b",
        "#1a1a2e", "#16213e", "#0f3460", "#2c3e50", "#1e3c72",
        "#27ae60", "#2ecc71", "#16a085", "#1abc9c",
        "background: #0", "background: #1", "background: #2", "background: #3",
    ]
    LIGHT_BG_KEYWORDS = [
        "#ecfdf5", "#d1fae5", "#f0fdfa", "#e6fffa", "#f8fffe",
        "#fff", "white", "#fafafa", "#f5f5f5", "#f0f0f0",
        "background: #e", "background: #f",
    ]

    for div in soup.find_all("div", style=True):
        st = div.get("style", "")
        st_lower = st.lower()
        is_dark = any(kw in st_lower for kw in DARK_BG_KEYWORDS)
        is_light = any(kw in st_lower for kw in LIGHT_BG_KEYWORDS)

        if is_dark and not is_light:
            # Fond sombre → forcer tout le texte en blanc
            for tag in div.find_all(["p", "span", "li", "strong", "b", "em", "i", "h1", "h2", "h3", "h4", "h5", "h6", "a"]):
                existing = tag.get("style", "")
                if "color" not in existing.lower():
                    tag["style"] = existing + "; color: #ffffff !important; text-shadow: 0 1px 3px rgba(0,0,0,0.2);"
        elif is_light:
            # Fond clair → forcer texte sombre
            for tag in div.find_all(["p", "span", "li", "strong", "b", "em"]):
                existing = tag.get("style", "")
                if "color: white" in existing.lower() or "color:#fff" in existing.lower().replace(" ", ""):
                    tag["style"] = existing + "; color: #1e293b !important; text-shadow: none;"

    # ── 2. Wrappers pour tableaux (réactivité + pas de débordement) ──
    for table in soup.find_all("table"):
        if not table.find_parent(class_="table-scroller"):
            wrapper = soup.new_tag("div", **{"class": "table-scroller"})
            table.wrap(wrapper)

    # ── 3. Restructuration DOM : wrapper report unique ──
    wrapper = soup.new_tag("div", id="report-wrapper")
    body = soup.body
    if body:
        # On déplace TOUT le contenu du body dans le wrapper sans exception
        # list() est nécessaire car on modifie l'itérable en extrayant les enfants
        for child in list(body.children):
            if child is not wrapper:
                wrapper.append(child.extract())
        body.insert(0, wrapper)

    # ── 4. Casser les classes Bootstrap qui cassent le layout ──
    for div in soup.find_all("div", class_="container"):
        classes = div.get("class", [])
        classes = [c for c in classes if c != "container"] + ["nb-inner"]
        div["class"] = classes

    # ── 5. Injection du CSS premium ──
    premium_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,700;1,9..144,900&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400&display=swap');

/* ═══════════════════════════════════════════════
   TOKENS DE DESIGN
   ═══════════════════════════════════════════════ */
:root {
    --teal-950:    #022c22;
    --teal-900:    #064e3b;
    --teal-700:    #047857;
    --teal-500:    #10b981;
    --teal-300:    #6ee7b7;
    --teal-100:    #d1fae5;
    --teal-50:     #ecfdf5;

    --slate-900:   #0f172a;
    --slate-700:   #334155;
    --slate-500:   #64748b;
    --slate-200:   #e2e8f0;
    --slate-100:   #f1f5f9;
    --slate-50:    #f8fafc;

    --gold:        #d97706;
    --gold-light:  #fef3c7;

    --radius-sm:   8px;
    --radius-md:   14px;
    --radius-lg:   22px;
    --radius-xl:   30px;

    --shadow-card: 0 4px 24px rgba(0,0,0,0.06), 0 1px 4px rgba(0,0,0,0.04);
    --shadow-lift: 0 12px 40px rgba(0,0,0,0.10), 0 2px 8px rgba(0,0,0,0.06);
    --shadow-deep: 0 24px 80px rgba(6,78,59,0.18), 0 4px 16px rgba(0,0,0,0.08);
}

/* ═══════════════════════════════════════════════
   BASE
   ═══════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
    background: #f0f9f6 !important;
    background-image:
        radial-gradient(ellipse 80% 60% at 20% 0%, rgba(16,185,129,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(4,120,87,0.06) 0%, transparent 60%) !important;
    margin: 0 !important;
    padding: 60px 20px !important;
    font-family: 'DM Sans', system-ui, sans-serif !important;
    color: var(--slate-700) !important;
    min-height: 100vh !important;
}

/* ═══════════════════════════════════════════════
   WRAPPER PRINCIPAL
   ═══════════════════════════════════════════════ */
#report-wrapper {
    max-width: 1300px !important;
    width: 96% !important;
    margin: 0 auto !important;
    background: #ffffff !important;
    padding: 72px 80px !important;
    border-radius: var(--radius-xl) !important;
    box-shadow: var(--shadow-deep) !important;
    border: 1px solid rgba(16,185,129,0.12) !important;
    position: relative !important;
    overflow: hidden !important;
}

/* Bande décorative verticale gauche */
#report-wrapper::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 5px;
    background: linear-gradient(180deg, #10b981 0%, #047857 50%, #022c22 100%);
    border-radius: 0 4px 4px 0;
}

/* Reset des conteneurs imbriqués du template nbconvert */
#report-wrapper .container,
#report-wrapper #notebook,
#report-wrapper #notebook-container,
#report-wrapper .nb-inner {
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

/* ═══════════════════════════════════════════════
   TYPOGRAPHIE — AUGMENTÉE POUR LISIBILITÉ
   ═══════════════════════════════════════════════ */
h1, .text_cell_render h1, .rendered_html h1 {
    font-family: 'Fraunces', Georgia, serif !important;
    font-size: 3.2rem !important;
    font-weight: 700 !important;
    color: var(--teal-900) !important;
    line-height: 1.1 !important;
    margin: 72px 0 32px 0 !important;
    letter-spacing: -0.8px !important;
}

h2, .text_cell_render h2, .rendered_html h2 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 600 !important;
    color: var(--slate-900) !important;
    margin: 64px 0 24px 0 !important;
    padding-bottom: 16px !important;
    border-bottom: 2px solid var(--teal-100) !important;
    display: flex !important;
    align-items: center !important;
    gap: 14px !important;
}

h2::before {
    content: '';
    display: inline-block !important;
    width: 10px !important;
    height: 10px !important;
    background: var(--teal-500) !important;
    border-radius: 50% !important;
    flex-shrink: 0 !important;
}

h3, .text_cell_render h3, .rendered_html h3 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.45rem !important;
    font-weight: 600 !important;
    color: var(--teal-700) !important;
    margin: 48px 0 16px 0 !important;
    letter-spacing: 0.1px !important;
}

h4, .text_cell_render h4, .rendered_html h4 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: var(--slate-500) !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    margin: 36px 0 12px 0 !important;
}

p, .text_cell_render p, .rendered_html p {
    font-size: 1.25rem !important;
    color: #334155 !important;
    line-height: 1.85 !important;
    margin-bottom: 20px !important;
    font-weight: 400 !important;
}

strong, b {
    color: #0f172a !important;
    font-weight: 700 !important;
    background: transparent !important;
}

/* Correction critique : strong/b dans les divs à fond coloré → blanc */
div[style*="background"] strong,
div[style*="background"] b,
div[style*="linear-gradient"] strong,
div[style*="linear-gradient"] b,
div[style*="background-color"] strong,
div[style*="background-color"] b {
    color: inherit !important;
}

em, i {
    color: #475569 !important;
    font-style: italic !important;
}

/* ── Spans & inline colorés dans le notebook ── */
span[style*="color"] {
    /* On force une lisibilité minimale sur fond blanc */
    filter: contrast(1.1) !important;
}

/* Texte sur fond coloré : toujours blanc */
[style*="background: #"] p,
[style*="background: rgb"] p,
[style*="background-color"] p,
[style*="background: linear-gradient"] p,
[style*="background: linear-gradient"] span,
[style*="background: linear-gradient"] li,
[style*="background: linear-gradient"] strong,
[style*="background: linear-gradient"] em {
    color: #ffffff !important;
    text-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
}

/* Cas spécifique : fond teal/vert clair → texte sombre */
[style*="background: #ecfdf5"] p,
[style*="background: #d1fae5"] p,
[style*="background: #f0fdfa"] p,
[style*="background:#ecfdf5"] p,
[style*="background:#d1fae5"] p,
[style*="background:#f0fdfa"] p {
    color: #064e3b !important;
    text-shadow: none !important;
}

/* Encadrés border-left : texte sombre sur fond clair */
div[style*="border-left"] p,
div[style*="border-left"] strong,
div[style*="border-left"] li,
div[style*="border-left"] span {
    color: #1e293b !important;
    text-shadow: none !important;
}

/* ═══════════════════════════════════════════════
   LISTES
   ═══════════════════════════════════════════════ */
ul, ol {
    padding-left: 20px !important;
    margin: 8px 0 20px 0 !important;
}

li {
    font-size: 1.2rem !important;
    color: var(--slate-700) !important;
    line-height: 1.8 !important;
    margin-bottom: 8px !important;
    padding-left: 6px !important;
}

ul li::marker { color: var(--teal-500) !important; font-size: 1.1em !important; }
ol li::marker { color: var(--teal-700) !important; font-weight: 700 !important; }

/* ═══════════════════════════════════════════════
   BANDEAUX À FOND COLORÉ (divs inline du notebook)
   ═══════════════════════════════════════════════ */
.text_cell_render div[style*="linear-gradient"],
.rendered_html div[style*="linear-gradient"] {
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-deep) !important;
    margin: 0 0 52px 0 !important;
}

.text_cell_render div[style*="linear-gradient"] *,
.rendered_html div[style*="linear-gradient"] * {
    color: #ffffff !important;
    border: none !important;
    text-shadow: 0 1px 4px rgba(0,0,0,0.2) !important;
}

/* Encadrés avec bordure gauche */
.text_cell_render div[style*="border-left"],
.rendered_html div[style*="border-left"] {
    border-radius: 0 var(--radius-md) var(--radius-md) 0 !important;
    background: var(--teal-50) !important;
    padding: 18px 24px !important;
    margin: 20px 0 !important;
}

blockquote {
    border-left: 4px solid var(--teal-500) !important;
    background: var(--teal-50) !important;
    padding: 18px 26px !important;
    margin: 24px 0 !important;
    border-radius: 0 var(--radius-md) var(--radius-md) 0 !important;
    color: var(--slate-700) !important;
    font-style: italic !important;
}

/* ═══════════════════════════════════════════════
   TABLEAUX
   ═══════════════════════════════════════════════ */
.table-scroller {
    overflow-x: auto !important;
    border-radius: var(--radius-md) !important;
    box-shadow: var(--shadow-card) !important;
    border: 1px solid var(--slate-200) !important;
    margin: 28px -20px !important;  /* déborde légèrement pour utiliser toute la largeur */
    width: calc(100% + 40px) !important;
}

.dataframe, table {
    font-family: 'DM Sans', sans-serif !important;
    border-collapse: collapse !important;
    width: 100% !important;
    min-width: 100% !important;
    margin: 0 !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
}

.dataframe thead tr, table thead tr {
    background: linear-gradient(135deg, var(--teal-900) 0%, var(--teal-700) 100%) !important;
}

.dataframe th, table th {
    background: transparent !important;
    color: #ffffff !important;
    padding: 16px 22px !important;
    text-align: left !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.4px !important;
    border: none !important;
    white-space: nowrap !important;
}

.dataframe td, table td {
    padding: 14px 22px !important;
    text-align: left !important;
    color: #1e293b !important;
    font-size: 0.92rem !important;
    font-weight: 450 !important;
    border-bottom: 1px solid var(--slate-200) !important;
    border-left: none !important;
    border-right: none !important;
    transition: background 0.12s !important;
}

.dataframe tbody tr:nth-child(even) td,
table tbody tr:nth-child(even) td {
    background: #f8fffe !important;
}

.dataframe tbody tr:hover td,
table tbody tr:hover td {
    background: var(--teal-50) !important;
}

/* ═══════════════════════════════════════════════
   GRAPHIQUES & OUTPUTS
   ═══════════════════════════════════════════════ */
.output_png img {
    border-radius: var(--radius-md) !important;
    box-shadow: var(--shadow-lift) !important;
    margin: 28px auto !important;
    display: block !important;
    max-width: 100% !important;
    border: 1px solid var(--slate-200) !important;
}

.plotly-graph-div {
    border-radius: var(--radius-md) !important;
    box-shadow: var(--shadow-lift) !important;
    margin: 28px 0 !important;
    border: 1px solid var(--slate-200) !important;
    overflow: hidden !important;
}

/* ═══════════════════════════════════════════════
   MASQUER CODE & PROMPTS
   ═══════════════════════════════════════════════ */
.input,
.prompt,
.input_prompt,
.output_prompt,
.jp-InputArea,
.jp-CodeCell .jp-InputArea,
div.input,
div.input_area,
pre.CodeMirror-line,
.CodeMirror {
    display: none !important;
}

pre {
    display: none !important;
}

/* Mais afficher les pre DANS les cellules Markdown (code inline) */
.text_cell_render pre,
.rendered_html pre {
    display: block !important;
    background: var(--slate-900) !important;
    color: #e2e8f0 !important;
    padding: 18px 22px !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.83rem !important;
    line-height: 1.6 !important;
    overflow-x: auto !important;
    margin: 16px 0 !important;
    box-shadow: var(--shadow-card) !important;
}

code {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85em !important;
    background: var(--teal-50) !important;
    color: var(--teal-900) !important;
    padding: 2px 7px !important;
    border-radius: 4px !important;
    border: 1px solid var(--teal-100) !important;
}

pre code {
    background: transparent !important;
    color: inherit !important;
    padding: 0 !important;
    border: none !important;
    border-radius: 0 !important;
}

/* ═══════════════════════════════════════════════
   CELLULES TEXTE — Espacement
   ═══════════════════════════════════════════════ */
.text_cell,
.cell.text_cell {
    padding: 4px 0 !important;
    margin-bottom: 4px !important;
}

.cell {
    margin-bottom: 0 !important;
    padding: 0 !important;
    border: none !important;
}

/* ═══════════════════════════════════════════════
   DIVIDER DÉCORATIF ENTRE SECTIONS
   ═══════════════════════════════════════════════ */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent 0%, var(--teal-300) 30%, var(--teal-300) 70%, transparent 100%) !important;
    margin: 48px 0 !important;
    opacity: 0.5 !important;
}

/* ═══════════════════════════════════════════════
   RESPONSIVE
   ═══════════════════════════════════════════════ */
@media (max-width: 900px) {
    body { padding: 20px 12px !important; }
    #report-wrapper { padding: 40px 28px !important; border-radius: var(--radius-lg) !important; }
    h1 { font-size: 1.8rem !important; }
    h2 { font-size: 1.15rem !important; }
    .dataframe, table { font-size: 0.82rem !important; }
    .table-scroller { margin: 28px 0 !important; width: 100% !important; }
}

/* ═══════════════════════════════════════════════
   IMPRESSION
   ═══════════════════════════════════════════════ */
@media print {
    body { background: white !important; padding: 0 !important; }
    #report-wrapper {
        max-width: 100% !important;
        box-shadow: none !important;
        border: none !important;
        padding: 20px !important;
        border-radius: 0 !important;
    }
    #report-wrapper::before { display: none !important; }
    .plotly-graph-div { break-inside: avoid !important; }
}
</style>
"""
    if soup.head:
        soup.head.append(BeautifulSoup(premium_css, "html.parser"))
    else:
        # Fallback : injecter le style en début de body
        style_tag = BeautifulSoup(premium_css, "html.parser")
        if soup.body:
            soup.body.insert(0, style_tag)

    return str(soup)


# ──────────────────────────────────────────────────────────────────────────────
# Compatibilité Windows (event loop asyncio)
# ──────────────────────────────────────────────────────────────────────────────
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# ──────────────────────────────────────────────────────────────────────────────
# Fonction principale : notebook → HTML
# ──────────────────────────────────────────────────────────────────────────────
def notebook_to_html_plotly(notebook_path, output_directory="rapport_html"):
    """
    Convertit un fichier Jupyter Notebook (.ipynb) en rapport HTML premium.

    Toutes les cellules sont exécutées, les graphiques Plotly sont conservés
    interactifs, le code source est masqué, et un design soigné est appliqué.

    Paramètres
    ----------
    notebook_path : str
        Chemin vers le fichier .ipynb à convertir.
    output_directory : str
        Dossier de destination du rapport HTML (créé si inexistant).

    Retour
    ------
    str
        Chemin complet vers le fichier HTML généré.

    Exceptions
    ----------
    FileNotFoundError
        Si notebook_path n'existe pas.
    nbformat.reader.NotJSONError
        Si le fichier n'est pas un notebook valide.
    """
    # Normalisation des chemins (sécurité Windows)
    notebook_path = os.path.normpath(notebook_path)
    output_directory = os.path.normpath(output_directory)

    if not os.path.isfile(notebook_path):
        raise FileNotFoundError(f"Notebook introuvable : {notebook_path}")

    # 1. Lecture du notebook
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    # 2. Exécution de toutes les cellules
    executor = ExecutePreprocessor(timeout=-1, allow_errors=False)
    executor.preprocess(notebook)

    # 3. Export HTML (template classique, sans code, sans prompts)
    html_exporter = HTMLExporter(template_name="classic")
    html_exporter.exclude_input = True
    html_exporter.exclude_input_prompt = True
    html_exporter.exclude_output_prompt = True
    # Ne PAS mettre exclude_output=True — cela supprimerait les graphiques !

    # Embed des widgets Plotly/ipywidgets dans le HTML
    resources = {"embed_widgets": True}
    body, _ = html_exporter.from_notebook_node(notebook, resources=resources)

    # 4. Post-traitement HTML
    body = remove_html_comments(body)
    body = apply_premium_design(body)

    # 5. Création du dossier de sortie si nécessaire
    os.makedirs(output_directory, exist_ok=True)

    # 6. Écriture du fichier HTML final
    notebook_name = os.path.splitext(os.path.basename(notebook_path))[0]
    html_file_path = os.path.join(output_directory, f"{notebook_name}.html")

    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(body)

    return html_file_path


# ──────────────────────────────────────────────────────────────────────────────
# Point d'entrée CLI
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    # Résolution automatique du chemin du notebook
    candidates = [
        "Analyse_Hospitaliere.ipynb",
        "../Analyse_Hospitaliere.ipynb",
    ]

    # Accepter un chemin en argument (ex: python generate_report.py mon_notebook.ipynb)
    if len(sys.argv) > 1:
        candidates = [sys.argv[1]] + candidates

    notebook_path = next((p for p in candidates if os.path.isfile(p)), None)

    if notebook_path is None:
        print(
            "ERROR: Impossible de trouver le notebook.\n"
            "   Utilisez : python generate_report.py <chemin_vers_notebook.ipynb>"
        )
        sys.exit(1)

    print(f"PROGRESS: Generation du rapport HTML depuis : {notebook_path} ...")

    try:
        output_path = notebook_to_html_plotly(notebook_path, output_directory="rapport_html")
        print(f"SUCCESS: Rapport genere avec succes : {output_path}")
    except FileNotFoundError as e:
        print(f"ERROR: Fichier introuvable : {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Erreur lors de la generation : {e}")
        sys.exit(1)