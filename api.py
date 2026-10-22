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
                                rec = dict(zip(FIELDS, parts))
                                records.append(rec)
                    except Exception:
                        pass
    print(f"[+] Loaded {len(records)} records")