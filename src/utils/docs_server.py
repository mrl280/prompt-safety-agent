import os

from flask import Flask, render_template, send_from_directory

from src.utils.paths import DOCS_DIR

app = Flask(__name__, template_folder=os.path.join(DOCS_DIR, "templates"))

print("DOCS_DIR =", DOCS_DIR)
print("Templates folder =", os.path.join(DOCS_DIR, "templates"))


@app.route("/")
def index():
    reports = ["report.html"]  # Example list, you can make this dynamic
    return render_template("index.html", reports=reports)


@app.route("/docs/<path:filename>")
def serve_docs(filename):
    return send_from_directory(DOCS_DIR, filename)
