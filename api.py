import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# ডেটা ফরম্যাট অনুযায়ী ফিল্ড লিস্ট — ১০টা (প্রথম ১০টা)
FIELDS = ["phone", "fb_id", "first_name", "last_name",
          "gender", "city", "area", "bio", "date", "extra"]

records = []

def load_all():
    global records
    records = []
    # data_parts ফোল্ডার + root দুইটাই চেক করবে
    search_dirs = ["data_parts", "."]
    for d in search_dirs:
        if os.path.isdir(d):
            for fname in sorted(os.listdir(d)):
                if fname.startswith("data_part_"):
                    path = os.path.join(d, fname)
                    try:
                        with open(path, "r", encoding="utf-8", errors="ignore") as f:
                            for line in f:
                                line = line.strip()
                                if not line:
                                    continue
                                parts = line.split(":")
                                parts += [""] * (len(FIELDS) - len(parts))
                                parts = parts[:len(FIELDS)]
                                rec = dict(zip(FIELDS, parts))
                                records.append(rec)
                    except Exception:
                        pass
    print(f"[+] Loaded {len(records)} records")

load_all()   # রান করানো

@app.route("/")
def home():
    return jsonify({"status": "API is running", "loaded": len(records)})

@app.route("/search")
def search():
    number = request.args.get("number", "").strip()
    if not number:
        return jsonify({"error": "number required"}), 400
    res = [r for r in records if r["phone"] == number]
    if not res:
        return jsonify({"error": "not found", "number": number}), 404
    return jsonify(res)

@app.route("/debug")
def debug():
    files = [f for d in ["data_parts", "."] if os.path.isdir(d)
             for f in os.listdir(d) if f.startswith("data_part_")]
    return jsonify({"loaded": len(records), "files_found": len(files)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
