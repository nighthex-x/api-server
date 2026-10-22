import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
SEARCH_DIRS = ["data_parts", "."]

# ডেটা ফরম্যাট অনুযায়ী ফিল্ড ম্যাপিং
def parse_line(line):
    parts = line.strip().split(":")
    # যতগুলো ফিল্ড পাওয়া যায়, ম্যাপ করি
    rec = {"phone": parts[0] if len(parts) > 0 else ""}
    keys = ["facebook_id", "first_name", "last_name", "gender",
            "city", "area", "nickname", "bio", "signup_date", "birthday"]
    for i, k in enumerate(keys):
        rec[k] = parts[i + 1] if len(parts) > i + 1 else ""
    return rec

def find_record(number):
    for d in SEARCH_DIRS:
        if not os.path.isdir(d):
            continue
        for fname in sorted(os.listdir(d)):
            if not fname.startswith("data_part_"):
                continue
            path = os.path.join(d, fname)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if line.startswith(number + ":"):
                            return parse_line(line)
            except Exception:
                continue
    return None

@app.route("/")
def home():
    return jsonify({"status": "API is running"})

@app.route("/search")
def search():
    number = request.args.get("number", "").strip()
    if not number:
        return jsonify({"error": "number required"}), 400
    rec = find_record(number)
    if not rec:
        return jsonify({"error": "not found", "number": number}), 404
    # আপনার ফরম্যাটে রেসপন্স
    return jsonify({
        "data": [rec],
        "credit": "BRH-Bangladesh"
    })

@app.route("/debug")
def debug():
    files = []
    for d in SEARCH_DIRS:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.startswith("data_part_"):
                    files.append(f)
    return jsonify({"files_found": len(files)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)