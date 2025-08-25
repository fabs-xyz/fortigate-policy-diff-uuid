# fortigate-policy-diff-uuid
A Python tool for comparing FortiGate firewall configuration files. Detects newly added, removed, and modified policies based on UUIDs and provides detailed diffs of policy blocks.

# FortiGate Policy Diff

A Python tool for comparing FortiGate firewall configuration files.  
It detects **new**, **removed**, and **modified** firewall policies based on their **UUIDs** and provides a detailed **line-by-line diff** of modified policy blocks.

## Features
- 🔎 Detects **new policies** (only in the new config)  
- 🗑️ Detects **removed policies** (only in the old config)  
- ✏️ Detects **modified policies** (same UUID but different content)  
- 📜 Shows differences directly in the terminal (Unified Diff format, similar to `git diff`)  

## Example Output // UUID and Name of the Firewall Policy

New policies:
a1b2c3d4-1234-5678-90ab-cdef12345678 (Allow_DNS)

Removed policies:
z9y8x7w6-9876-5432-10ab-cdef98765432 (Block_FTP)
