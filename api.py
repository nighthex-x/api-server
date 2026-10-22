import os
from flask import Flask, request, jsonify

app = Flask(__name__)

SEARCH_DIRS = ["data_parts", "."]

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
 return line.strip()
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
 line = find_record(number)
 if not line:
 return jsonify({"error": "not found", "number": number}), 404
 parts = line.split(":")
 return jsonify({"number": number, "data": parts})

@app.route("/debug")
def debug():
 files = [f for d in SEARCH_DIRS if os.path.isdir(d)
 for f in os.listdir(d) if f.startswith("data_part_")]
 return jsonify({"files_found": len(files)})

if __name__ == "__main__":
 port = int(os.environ.get("PORT", 10000))
 app.run(host="0.0.0.0", port=port)
