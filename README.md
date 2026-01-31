# MANDORA v0.2.1 - Adaptive Directory Bruteforcing Toolkit

**MANDORA** is a powerful, modular tool for directory bruteforcing. It’s designed for ethical hackers, bug bounty hunters, and cybersecurity learners.

> **Status:** v0.2.1 (Active development)
> **Purpose:** Ethical hacking & educational use only

---

## 🔑 Features

* Layered brute force with soft-404 fingerprinting to reduce redirect noise
* WAF detection powered by `wafw00f` with focused vendor reporting
* Header rotation and optional proxy pool (`MANDORA_PROXIES`) for evasive scanning
* Depth-controlled enumeration (1–4) with per-depth results and summaries
* Graceful interrupt handling with persistent output and stats recap
* Modular Python codebase for easy upgrades

---

## 📁 Layout

```
MANDORA/
├── mandora.py            # CLI entry point
├── core/
│   ├── scanner.py        # Directory discovery engine
│   └── waf_detector.py   # WAF identification bridge
├── wordlists/
│   └── wordlists.txt     # Default brute-force terms
├── output/               # Scan artefacts (created at runtime)
├── CHANGELOG.md          # Release notes
├── README.md             # Documentation
├── requirements.txt      # Dependencies
└── LICENSE               # GPL-3.0 license
```

---

## ⚙️ Setup

### 1. Clone & Enter Directory

```bash
git clone https://github.com/mandal-suman/MANDORA.git
cd MANDORA
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Confirm the CLI boots

```bash
python mandora.py
```

You can override the default proxies by exporting `MANDORA_PROXIES="http://127.0.0.1:8080, socks5://127.0.0.1:1080"`.

---

## 📝 Wordlist Tips

- Start from `wordlists/wordlists.txt` and extend with tech-aware endpoints
- Keep entries lowercase unless the target is case-sensitive
- For niche apps, import bigger lists via `--wordlist` (coming soon) or replace the default file

---

## 🚀 How to Use

```bash
python mandora.py
```

**Prompts:**

1. Target URL (scheme optional; defaults to https)
2. Depth (1–4)

**Sample Output:**

```
=== MANDORA: Directory Bruteforcer with WAF Detection ===
🌐 Enter target site (e.g., https://example.com): https://demo.target
🔍 Running WAF detection...
🔒 WAF detected:
 - Cloudflare (vendor=Cloudflare Inc.)
✅ Wordlists loaded successfully
[+] Found (depth 1): https://demo.target/admin [status 200]
[~] Redirected to https://demo.target/home from https://demo.target/admin/login
[-] Soft 404 detected: https://demo.target/secret

--- Scan Summary ---
Total requests: 50
Valid hits: 3
Protected hits: 1
Redirects skipped: 7
Soft 404 filtered: 6
Processing errors: 0

📁 Output saved in: output/demo_target
```

---

## 📦 Output Format

```
output/
└── demo_target/
    ├── waf_detected.txt      # summarised WAF signals
    ├── depth_1.txt           # URLs discovered at depth 1
    └── depth_2.txt           # ...and so on
```

- Each line contains the URL, status, and classification note
- Results persist even if you abort mid-scan

---

### Depth Strategy

- Depth 1: /admin
- Depth 2: /admin/panel
- Depth 3: /admin/panel/config
- Depth 4: /admin/panel/config/database

---

## ⚠️ Legal Use

- Scan only assets you own or have explicit permission to test
- Observe local laws and responsible disclosure best practices
- Respect rate limits and pause if targets degrade

---

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch off `main`
3. Add tests or sample output where relevant
4. Open a pull request with context and reproduction steps

**Wish list:** multithreaded mode, alternative output formats, custom headers per target, resumable sessions

---

## 👤 Author

- Suman Mandal — cybersecurity learner and open-source contributor
- GitHub: [@mandal-suman](https://github.com/mandal-suman)

---

## 🙏 Acknowledgements

- `wafw00f` maintainers for robust WAF detection heuristics
- `requests` ecosystem contributors
- Community testers providing feedback on redirect edge cases

---

**Built for responsible reconnaissance — January 2026**
