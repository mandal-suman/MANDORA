# MANDORA v1.0 - Advanced Directory Bruteforcing Tool

**MANDORA** is a powerful, modular tool for directory bruteforcing. It’s designed for ethical hackers, bug bounty hunters, and cybersecurity learners.

> **Status:** v1.0 (Stable release)
> **Purpose:** Ethical hacking & educational use only

---

## 🔑 Features

* Brute-force hidden web directories using wordlists
* Detect Web Application Firewalls (WAF) with `wafw00f`
* Scan up to 4 directory levels deep
* Save results in structured folders by domain
* Modular Python codebase for easy updates
* Real-time progress output

---

## 📁 File Structure

```
MANDORA/
├── mandora.py            # Main script
├── requirements.txt      # Dependencies
├── README.md             # Docs
├── LICENSE               # GPL-3.0 license
├── .gitignore            # Git ignore file
├── wordlists/
│   └── wordlists.txt     # Default wordlist
├── output/               # Scan results
└── core/
    ├── __init__.py       # Init
    ├── scanner.py        # Scanning logic
    └── waf_detector.py   # WAF detection
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

### 3. Test Installation

```bash
python mandora.py
```

---

## 📝 Wordlist

**File:** `wordlists/wordlists.txt`

**Examples:**

```
admin
login
dashboard
api
config
```

**Tips:**

* Use lowercase
* Add target-specific and tech-specific terms

---

## 🚀 How to Use

```bash
python mandora.py
```

**Prompts:**

1. Enter target URL
2. Select depth (1–4)

**Sample Output:**

```
🌐 https://testsite.com
✅ WAF: None
✅ Wordlist loaded
[+] Found: /admin
[+] Found: /admin/uploads
📁 Saved to: output/testsite_com
```

---

## 📦 Output Format

```
output/
└── testsite_com/
    ├── waf_detected.txt
    ├── depth_1.txt
    ├── depth_2.txt
    └── scan_summary.txt
```

* Plain text URLs
* Timestamped
* Status codes included

---

### Scan Depth Strategy

* Depth 1: /admin
* Depth 2: /admin/panel
* Depth 3: /admin/panel/config
* Depth 4: /admin/panel/config/database

---

## ⚠️ Legal Use Only

* Test only what you **own or have permission** to scan
* Always follow ethical hacking guidelines
* Never target unauthorized systems

---

## 🤝 Contribute

1. Fork and clone the repo
2. Create a branch and add your changes
3. Submit a pull request

**Ideas:**

* Speed improvements
* JSON/CSV output
* WAF bypass
* Error handling

---

## 👤 Author

**Suman Mandal** – Cybersecurity student & open-source enthusiast

GitHub: [@sumanmandal](https://github.com/mandal-suman)

---

## 📌 Roadmap

* **v1.1:** Multithreading, rate limits, better error handling
* **v1.2+:** Subdomain scan, export formats, config files
* **v2.0:** GUI/web interface, cloud use, team collaboration

---

## 🙏 Thanks To

* `wafw00f` project
* `requests` library maintainers
* Cybersecurity community

---

**Built with ❤️ for the hacking community – May 2025**
