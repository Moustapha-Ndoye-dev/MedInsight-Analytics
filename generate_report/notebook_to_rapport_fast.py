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
    soup = BeautifulSoup(html_content, "html.parser")
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    return str(soup)


# ──────────────────────────────────────────────────────────────────────────────
# Transformation du DOM + injection CSS premium
# ──────────────────────────────────────────────────────────────────────────────
def apply_premium_design(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    for div in soup.find_all("div", style=True):
        st = div.get("style", "").lower()
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
        if "border-left" in st:
            for old, new in [("#2ecc71", "#0d9488"), ("#1e3c72", "#0d9488"), ("#f8fbfa", "#ecfdf5"), ("#27ae60", "#059669")]:
                div["style"] = div["style"].replace(old, new)

    DARK_BG_KEYWORDS = ["linear-gradient", "#0d9488", "#065f46", "#047857", "#064e3b"]
    for div in soup.find_all("div", style=True):
        st_lower = div.get("style", "").lower()
        if any(kw in st_lower for kw in DARK_BG_KEYWORDS):
            for tag in div.find_all(["p", "span", "li", "strong", "b", "em"]):
                existing = tag.get("style", "")
                if "color" not in existing.lower():
                    tag["style"] = existing + "; color: #ffffff !important;"

    for table in soup.find_all("table"):
        if not table.find_parent(class_="table-scroller"):
            wrapper = soup.new_tag("div", **{"class": "table-scroller"})
            table.wrap(wrapper)

    wrapper = soup.new_tag("div", id="report-wrapper")
    body = soup.body
    if body:
        for child in list(body.children):
            if child is not wrapper:
                wrapper.append(child.extract())
        body.insert(0, wrapper)

    premium_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@700&family=DM+Sans:wght@400;500;700&family=JetBrains+Mono&display=swap');
:root {
    --teal-900: #064e3b; --teal-700: #047857; --teal-500: #10b981; --teal-50: #ecfdf5;
    --slate-900: #0f172a; --slate-700: #334155; --slate-200: #e2e8f0;
}
body { background: #f0f9f6 !important; font-family: 'DM Sans', sans-serif !important; padding: 60px 20px !important; }
#report-wrapper { max-width: 1200px !important; margin: 0 auto !important; background: white !important; padding: 60px !important; border-radius: 30px !important; box-shadow: 0 20px 80px rgba(6,78,59,0.1) !important; position: relative !important; overflow: hidden !important; border: 1px solid rgba(16,185,129,0.1) !important; }
#report-wrapper::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 6px; background: linear-gradient(180deg, #10b981, #064e3b); }
h1 { font-family: 'Fraunces', serif !important; font-size: 3rem !important; color: var(--teal-900) !important; }
h2 { border-bottom: 2px solid var(--teal-50) !important; padding-bottom: 10px !important; color: var(--slate-900) !important; }
.input, .prompt, .input_prompt, .output_prompt { display: none !important; }
.dataframe, table { border-collapse: collapse !important; width: 100% !important; margin: 20px 0 !important; }
.dataframe th { background: var(--teal-900) !important; color: white !important; padding: 12px !important; }
.dataframe td { padding: 10px !important; border-bottom: 1px solid var(--slate-200) !important; }
.table-scroller { overflow-x: auto !important; }
</style>
"""
    if soup.head:
        soup.head.append(BeautifulSoup(premium_css, "html.parser"))
    return str(soup)

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def notebook_to_html_plotly(notebook_path, output_directory="rapport_html"):
    if not os.path.isfile(notebook_path):
        raise FileNotFoundError(f"Notebook introuvable : {notebook_path}")

    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    # SKIP EXECUTION FOR SPEED
    # executor = ExecutePreprocessor(timeout=-1, allow_errors=False)
    # executor.preprocess(notebook)

    html_exporter = HTMLExporter(template_name="classic")
    html_exporter.exclude_input = True
    html_exporter.exclude_input_prompt = True
    html_exporter.exclude_output_prompt = True

    body, _ = html_exporter.from_notebook_node(notebook)

    body = remove_html_comments(body)
    body = apply_premium_design(body)

    os.makedirs(output_directory, exist_ok=True)
    notebook_name = os.path.splitext(os.path.basename(notebook_path))[0]
    html_file_path = os.path.join(output_directory, f"{notebook_name}.html")

    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(body)

    return html_file_path

if __name__ == "__main__":
    import sys
    notebook_path = sys.argv[1] if len(sys.argv) > 1 else "Analyse_Hospitaliere.ipynb"
    print(f"PROGRESS: Generation RAPIDE du rapport (sans execution) : {notebook_path} ...")
    try:
        output_path = notebook_to_html_plotly(notebook_path, output_directory="rapport_html")
        print(f"SUCCESS: Rapport genere avec succes : {output_path}")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
