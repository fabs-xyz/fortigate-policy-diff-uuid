import re


def extract_policies(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Alle Policy-Blöcke (edit ... next)
    blocks = re.findall(r'(edit \d+.*?next)', content, re.S)
    policies = {}

    for block in blocks:
        policy = parse_policy_block(block)
        if "uuid" in policy:
            policies[policy["uuid"]] = policy

    return policies


def parse_policy_block(block):
    data = {}
    # Relevante Felder definieren
    fields = [
        "uuid",
        "name",
        "srcintf",
        "dstintf",
        "srcaddr",
        "dstaddr",
        "service",
        "schedule",
        "action",
    ]

    for field in fields:
        match = re.search(rf'set {field} (.+)', block)
        if match:
            value = match.group(1).strip().strip('"')
            data[field] = value
    return data


def print_table(header, rows):
    """Einfache Tabellenausgabe ohne externe Bibliotheken"""
    if not rows:
        print("Keine\n")
        return

    # Spaltenbreiten berechnen
    col_widths = [len(h) for h in header]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    # Formatstring bauen
    fmt = "  ".join("{:<" + str(w) + "}" for w in col_widths)

    # Header + Trenner
    print(fmt.format(*header))
    print("  ".join("-" * w for w in col_widths))

    # Zeilen
    for row in rows:
        print(fmt.format(*row))
    print()


# Configs laden
old = extract_policies("old.conf")
new = extract_policies("new.conf")

old_uuids = set(old.keys())
new_uuids = set(new.keys())

new_only = new_uuids - old_uuids
old_only = old_uuids - new_uuids
common = old_uuids & new_uuids

# Unterschiede finden
changed = []
for uuid in common:
    if old[uuid] != new[uuid]:
        changed.append(uuid)

# Ausgabe
print("Neue Policies:")
rows = [[u, new[u].get("name", "")] for u in sorted(new_only)]
print_table(["UUID", "Name"], rows)

print("Entfernte Policies:")
rows = [[u, old[u].get("name", "")] for u in sorted(old_only)]
print_table(["UUID", "Name"], rows)

print("Geänderte Policies:")
if changed:
    for u in changed:
        diffs = []
        for k in set(old[u].keys()) | set(new[u].keys()):
            old_val = old[u].get(k, "")
            new_val = new[u].get(k, "")
            if old_val != new_val:
                diffs.append([k, old_val, new_val])
        print(f"\nUUID: {u} ({old[u].get('name', '')})")
        print_table(["Feld", "Alt", "Neu"], diffs)
else:
    print("Keine Änderungen\n")
