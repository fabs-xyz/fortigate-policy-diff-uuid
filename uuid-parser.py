import re

def extract_policies(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match all policy blocks (edit ... next)
    blocks = re.findall(r'(edit \d+.*?next)', content, re.S)
    policies = {}

    for block in blocks:
        policy = parse_policy_block(block)
        if "uuid" in policy:
            policies[policy["uuid"]] = policy

    return policies


def parse_policy_block(block):
    data = {}
    # Relevant fields
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


def format_table(header, rows):
    """Format table output without external libraries"""
    if not rows:
        return "None\n"

    # Calculate column widths
    col_widths = [len(h) for h in header]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    # Build format string
    fmt = "  ".join("{:<" + str(w) + "}" for w in col_widths)

    # Header + separator
    output = []
    output.append(fmt.format(*header))
    output.append("  ".join("-" * w for w in col_widths))

    # Rows
    for row in rows:
        output.append(fmt.format(*row))
    output.append("")
    return "\n".join(output)


def main():
    # Load configs
    old = extract_policies("old.conf")
    new = extract_policies("new.conf")

    old_uuids = set(old.keys())
    new_uuids = set(new.keys())

    new_only = new_uuids - old_uuids
    old_only = old_uuids - new_uuids
    common = old_uuids & new_uuids

    # Find changed policies
    changed = []
    for uuid in common:
        if old[uuid] != new[uuid]:
            changed.append(uuid)

    output_lines = []

    # New policies
    output_lines.append("New Policies:")
    rows = [[u, new[u].get("name", "")] for u in sorted(new_only)]
    output_lines.append(format_table(["UUID", "Name"], rows))

    # Removed policies
    output_lines.append("Removed Policies:")
    rows = [[u, old[u].get("name", "")] for u in sorted(old_only)]
    output_lines.append(format_table(["UUID", "Name"], rows))

    # Changed policies
    output_lines.append("Changed Policies:")
    if changed:
        for u in changed:
            diffs = []
            for k in set(old[u].keys()) | set(new[u].keys()):
                old_val = old[u].get(k, "")
                new_val = new[u].get(k, "")
                if old_val != new_val:
                    diffs.append([k, old_val, new_val])
            output_lines.append(f"\nUUID: {u} ({old[u].get('name', '')})")
            output_lines.append(format_table(["Field", "Old", "New"], diffs))
    else:
        output_lines.append("None\n")

    final_output = "\n".join(output_lines)

    # Print to console
    print(final_output)

    # Save to file
    with open("policy_diff.txt", "w", encoding="utf-8") as f:
        f.write(final_output)


if __name__ == "__main__":
    main()
