import os
from flask import Flask, request, jsonify

app = Flask(__name__)

DATA_DIR = "data_parts"
records = []

FIELDS = ["phone", "facebook_id", "first_name", "last_name", "gender",
          "city", "area", "nickname", "bio", "signup_date", "birthday"]

def load_all():
    global records
    records = []
    if os.path.isdir(DATA_DIR):
        for fname in sorted(os.listdir(DATA_DIR)):
            if fname.startswith("data_part_"):
                path = os.path.join(DATA_DIR, fname)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            parts = line.split(":")
                            parts += [""] * (len(FIELDS) - len(parts))
                            rec = dict(zip(FIELDS, parts))
                            records.append(rec)
                except Exception:
                    pass
    print(f"[+] Loaded {len(records)} records")

load_all()

@app.route("/")
def index():
    return "API is running ✅"

@app.route("/search")
def search():
    # "phone" বা "number" — দুটাই কাজ করবে
    num = request.args.get("number") or request.args.get("phone")
    num = (num or "").strip()

    if not num:
        return jsonify({"error": "number or phone required"}), 400

    for r in records:
        if r["phone"] == num:
            return jsonify({"data": [r], "credit": "BRH-Bangladesh"})

    return jsonify({"message": "not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))