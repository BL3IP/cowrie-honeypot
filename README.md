# 03 — SSH/Telnet Honeypot (Cowrie) + Captured Attack

A **Cowrie** honeypot deployed with Docker, attacked with a simulated SSH brute-force +
post-exploitation session, and the captured attacker telemetry saved as evidence.

## Goal
Stand up a medium-interaction honeypot, generate a realistic attack against it, and show the
high-value telemetry it captures (credentials tried, commands run) — exactly what a honeypot
provides a blue team / threat-intel program.

## Exact Setup Commands
```powershell
cd C:\Users\banlv\cyber\03-honeypot
docker compose up -d                       # starts Cowrie on :2222 (SSH) / :2223 (telnet)

# simulate an attacker (brute force + commands) against your own honeypot:
& "C:\Users\banlv\AppData\Local\Programs\Python\Python312\python.exe" -m venv .venv
.\.venv\Scripts\python.exe -m pip install paramiko
.\.venv\Scripts\python.exe attack\brute_force.py

# view what Cowrie captured:
docker logs cowrie
docker cp cowrie:/cowrie/cowrie-git/var/log/cowrie/cowrie.json .\artifacts\cowrie.json
```

## Proof It Works
The simulated attack ([`attack/brute_force.py`](./attack/brute_force.py)) was fully captured —
**3 connections, 1 failed + 2 successful logins, 2 commands** ([`artifacts/captured-attacks.log`](./artifacts/captured-attacks.log),
structured [`artifacts/cowrie.json`](./artifacts/cowrie.json)):
```
New connection: 172.17.0.1 ... (session: 7125af51dcb2)
login attempt [root/123456] failed
login attempt [admin/admin] succeeded        CMD: whoami
login attempt [root/letmein123] succeeded     CMD: whoami
```
Cowrie logs the **source IP, every credential tried, and every command** an attacker runs in the
fake shell — turning intrusion attempts into actionable intelligence.

## Screenshots
See [`./screenshots/`](./screenshots). Add: the `docker logs cowrie` output and the JSON events.
For a real deployment, screenshot the live attacks on a VPS and a Grafana/Kibana dashboard.

## My Custom Extensions
- A reproducible **attack simulator** (paramiko) so the capture is demonstrable offline — not just
  "deploy and wait".
- Both human-readable and **structured JSON** telemetry saved for ingestion (SIEM/threat-intel).
- Compose maps SSH+Telnet; documented volume mount + port-22 mapping for a real internet-facing host.

## Resume Bullet Points
- Deployed a **Cowrie** medium-interaction SSH/Telnet honeypot via Docker and captured a simulated
  brute-force + post-exploitation session (credentials + executed commands).
- Produced structured (JSON) attacker telemetry suitable for SIEM/threat-intel ingestion.
- Built a reproducible attack simulator to demonstrate detection end-to-end.

## Next-Level Ideas
- Deploy on a cheap internet-facing VPS and collect real-world attacks ("captured nation-state IPs").
- Ship cowrie.json to the SIEM and build a Grafana dashboard of top usernames/passwords/commands.
- Enrich captured source IPs with `iocsift` and the threat-intel brief (project 09).

---
status: ✅ complete & tested
```
✅ PROJECT COMPLETE & FULLY TESTED in its isolated folder. All works. Ready for portfolio.
```
