from flask import Flask, render_template, redirect, url_for
import json, os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(APP_DIR, "data", "publicacoes.json")

app = Flask(__name__)

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    pubs = load_data()
    pubs.sort(key=lambda x: x.get("data",""), reverse=True)
    return render_template("index.html", pubs=pubs)

@app.route("/toggle/<int:pub_id>")
def toggle(pub_id):
    pubs = load_data()
    for p in pubs:
        if p.get("id") == pub_id:
            p["status"] = "Providenciado" if p.get("status") != "Providenciado" else "Aguardando providência"
            break
    save_data(pubs)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
