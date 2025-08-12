import os

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
    Read a markdown file and convert to HTML.
    """
    md_path = os.path.join(CONTENT_DIR, md_filename)
    if not os.path.isfile(md_path):
        abort(404)

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    return markdown.markdown(md_text)


@app.route("/")
def index():
    return redirect("/docs/introduction.html")


@app.route("/docs/<page>.html")
def render_page(page):
    """Render a specific markdown page as HTML."""
    md_filename = f"{page}.md"
    if md_filename not in PAGE_ORDER:
        abort(404)

    html_content = md_to_html(md_filename)
    page_title = page.replace("-", " ").title()
    return render_template(
        "base.html",
        title=page_title,
        heading=page_title,
        content=html_content,
    )


if __name__ == "__main__":
    # Runw with Flask's built-in development server
    app.run(host="0.0.0.0", port=8000, debug=True)
