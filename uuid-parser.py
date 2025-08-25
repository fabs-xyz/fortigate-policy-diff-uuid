import re

def extract_policies(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # alle Policy-Blöcke (von edit ... next)
    blocks = re.findall(r'(edit .*? next)', content, re.S)
    policies = {}

    for block in blocks:
        uuid_match = re.search(r'set uuid (\S+)', block)
        name_match = re.search(r'set name "(.*?)"', block)

        if uuid_match:
            uuid = uuid_match.group(1)
            name = name_match.group(1) if name_match else "(kein Name)"
            policies[uuid] = name

    return policies


# Configs laden
old = extract_policies("old.conf")
new = extract_policies("new.conf")

old_uuids = set(old.keys())
new_uuids = set(new.keys())

new_only = new_uuids - old_uuids
old_only = old_uuids - new_uuids

print("new hinzugekommen:")
for u in sorted(new_only):
    print(f"- {u}  ({new[u]})")

print("\nEntfernt:")
for u in sorted(old_only):
    print(f"- {u}  ({old[u]})")
