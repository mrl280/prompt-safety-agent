import os
import re

import markdown
from flask import Flask, abort, redirect, render_template

app = Flask(__name__, template_folder="templates")

# Base directory for markdown content inside the docs folder
CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content")

PAGE_ORDER = [
    "introduction.md",
    "dataset-exploration.md",
    "tdidf-classifier.md",
    "llm-classifier.md",
    "integrated-pipline.md",
    "conclusion.md",
]


def md_to_html(md_filename):
    """
    Convert Markdown to HTML.
    """
    md_path = os.path.join(CONTENT_DIR, md_filename)
    if not os.path.isfile(md_path):
        abort(404)

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    return markdown.markdown(
        md_text,
        extensions=["fenced_code", "pymdownx.highlight", "pymdownx.arithmatex"],
        extension_configs={"pymdownx.arithmatex": {"generic": True}},  # Leave math as raw tex for MathJax to render
    )


def insert_plots(html):
    """
    Replace plot placeholders in HTML with actual Plotly plot contents.
    """

    def repl(match):
        plot_file = match.group(1)
        plot_path = os.path.join(CONTENT_DIR, "plots", plot_file)
        if os.path.isfile(plot_path):
            with open(plot_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return f"<p><strong>Plot file {plot_file} not found.</strong></p>"

    pattern = re.compile(r"\{\{\s*plot:(.+?)\s*\}\}")
    return pattern.sub(repl, html)


@app.route("/")
def index():
    """
    Redirect page root to the Introduction page.
    """
    return redirect("/introduction.html")


@app.route("/<page>.html")
def render_page(page):
    """
    Render a specific markdown page as HTML.
    """
    md_filename = f"{page}.md"
    if md_filename not in PAGE_ORDER:
        abort(404)

    html_content = md_to_html(md_filename)
    html_content = insert_plots(html_content)
    page_title = page.replace("-", " ").title()
    return render_template(
        "base.html",
        title=page_title,
        heading=page_title,
        content=html_content,
    )


if __name__ == "__main__":
    # Run with Flask's built-in development server
    app.run(host="0.0.0.0", port=8000, debug=True)
