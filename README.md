# FortiGate Policy Diff

A Python tool for comparing FortiGate firewall configuration files.  
It detects **new**, **removed**, and **modified** firewall policies based on their **UUIDs** and provides a detailed **attribute-level diff** of modified policy blocks.

## Features
- 🔎 Detects **new policies** (only in the new config)  
- 🗑️ Detects **removed policies** (only in the old config)  
- ✏️ Detects **modified policies** (same UUID but different content)  
- 📊 Shows differences in a clear **table format**  
- 📝 Exports the full diff to a text file (`policy_diff.txt`)  

## Instructions
1. Place the script together with the old FortiGate configuration (`old.conf`) and new FortiGate configuration (`new.conf`) in the same folder.  
2. Run the script:  

```bash
python policy_diff.py
```
3. Results will be printed in the terminal and written to policy_diff.txt.

Example Output // UUID and Name of the Firewall Policy
New Policies
UUID                                   Name
------------------------------------  ---------------
d0f74f64-fc41-51e9-2dfc-729f027e9979  Allow_DNS

Removed Policies
UUID                                   Name
------------------------------------  ---------------
a9c12b73-8d11-4f5d-bc24-12f4e98e10ab  Block_FTP

Changed Policies
UUID: e3f21d54-7b29-4c1d-8f6a-91b4d23a87ef (Web_Access)

Field     Old        New
--------  ---------  ---------
action    deny       accept
service   HTTP       HTTP,HTTPS
