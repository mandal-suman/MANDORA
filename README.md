# 🕵️‍♂️ MANDORA v1.0 - Advanced Directory Bruteforcing Tool

**MANDORA** is a modular and depth-controlled directory bruteforcing tool designed for cybersecurity professionals, bug bounty hunters, and ethical hackers. It combines traditional brute-forcing with advanced features like WAF detection and structured output logging, helping you identify hidden endpoints with precision and clarity.

> 🔰 **Project Status:** v1.0 (Initial stable release)  
> 🛡️ **Built for:** Ethical penetration testing and educational purposes only

---

## 📌 Key Features

- 🔍 **Directory Bruteforcing** – Test thousands of potential paths against target web servers using custom wordlists
- 🔒 **WAF Detection** – Integrated `wafw00f` to detect Web Application Firewalls before scanning
- 🎯 **Depth-Controlled Scanning** – Scan up to 4 levels deep in directory structures (`/admin/upload/images/`)
- 📁 **Organized Output** – Structured folder organization by domain and scan depth
- ⚙️ **Modular Architecture** – Clean, reusable code separated into logical modules
- 📊 **Real-time Feedback** – Live status updates during scanning process

---

## 📂 Project Structure

```
MANDORA/
│
├── mandora.py                 # Main script (entry point)
├── requirements.txt           # Python dependencies
├── README.md                  # This documentation
├── LICENSE                    # MIT License
├── .gitignore                 # Git ignore rules
│
├── wordlists/
│   └── wordlists.txt         # Custom wordlist (one entry per line)
│
├── output/                   # Scan results saved here
│   └── [domain_folders]/     # Organized by target domain
│
└── core/
    ├── __init__.py           # Package initialization
    ├── scanner.py            # Main scanning logic
    └── waf_detector.py       # WAF detection using wafw00f
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/mandal-suman/MANDORA.git
cd MANDORA
```

### 2. Install Dependencies
```bash pip install -r requirements.txt```

**requirements.txt contents:**

```requests>=2.28.0 
wafw00f>=2.2.0```

### 3. Verify Installation

```bash
python mandora.py --help
```

---

## 📝 Wordlist Configuration

MANDORA uses simple line-by-line text files as wordlists. Customize or replace the default wordlist:

**Location:** `wordlists/wordlists.txt`

**Sample entries:**
```
admin
login
uploads
dashboard
api
config
backup
test
dev
staging
panel
management
secure
private
hidden
```

**Tips for effective wordlists:**
- Use common directory names first
- Include technology-specific paths (e.g., `wp-admin` for WordPress)
- Consider target-specific terminology
- Keep entries lowercase for consistency

---

## 🚀 Usage Guide

### Basic Usage

```bash
python mandora.py
```

### Interactive Prompts

1. **Target URL Input:**
   ```
   🌐 Enter target site (e.g., https://example.com): https://testsite.com
   ```

2. **Depth Selection:**
   ```
   Enter max depth (1 to 4): 2
   ```

### Sample Execution Flow

```bash
$ python mandora.py

🌐 Enter target site (e.g., https://example.com): https://testsite.com
Enter max depth (1 to 4): 2

🔍 Running WAF detection...
✅ No WAF detected (or not identifiable)
✅ Wordlists loaded successfully

[+] Found (depth 1): https://testsite.com/admin
[-] Not Found (404): https://testsite.com/uploads
[+] Found (depth 2): https://testsite.com/admin/uploads
[+] Found (depth 2): https://testsite.com/admin/config

📁 Output saved in: output/testsite_com
🎯 Scan completed successfully!
```

---

## 📁 Output Structure & Format

Results are automatically organized in the `/output/` directory:

```
output/
└── testsite_com/
    ├── waf_detected.txt       # WAF detection results
    ├── depth_1.txt            # Found URLs at depth 1
    ├── depth_2.txt            # Found URLs at depth 2
    ├── depth_3.txt            # Found URLs at depth 3 (if applicable)
    ├── depth_4.txt            # Found URLs at depth 4 (if applicable)
    └── scan_summary.txt       # Overall scan statistics
```

**File content format:**
- **Plain text URLs** (one per line)
- **Timestamp** at the beginning of each file
- **HTTP status codes** included for context
- **Clean, parseable format** for further analysis

---

## 🔧 Advanced Configuration

### Custom Wordlists

Replace or add wordlists in the `wordlists/` folder:

```bash
# Use custom wordlist
cp /path/to/your/custom_wordlist.txt wordlists/wordlists.txt
```

### Depth Strategy

- **Depth 1:** `/admin`, `/login`, `/api`
- **Depth 2:** `/admin/panel`, `/api/v1`, `/login/secure`
- **Depth 3:** `/admin/panel/config`, `/api/v1/users`
- **Depth 4:** `/admin/panel/config/database`

**Recommendation:** Start with depth 2-3 for most targets to balance thoroughness with scan time.

---

## 🛡️ Security & Legal Disclaimer

**⚠️ CRITICAL: READ BEFORE USE**

MANDORA is built **strictly for educational and authorized penetration testing purposes only.**

### Legal Requirements

- ✅ **Only scan systems you own** or have explicit written permission to test
- ✅ **Obtain proper authorization** before any security assessment
- ✅ **Respect rate limits** and avoid overwhelming target servers
- ❌ **Never use on unauthorized targets** - this is illegal and unethical

### Responsible Usage

- Follow your organization's security testing guidelines
- Document all testing activities properly
- Report findings through appropriate channels
- Respect bug bounty program rules and scope

**The author assumes no responsibility for misuse of this tool.**

---

## 🤝 Contributing to MANDORA

We welcome contributions from the cybersecurity community!

### How to Contribute

1. **🍴 Fork the repository**
   ```bash
   git clone https://github.com/yourusername/MANDORA.git
   ```

2. **🛠️ Create a feature branch**
   ```bash
   git checkout -b feature/your-improvement
   ```

3. **💾 Make your changes and commit**
   ```bash
   git commit -m "Add: Your feature description"
   ```

4. **🚀 Push and create a pull request**
   ```bash
   git push origin feature/your-improvement
   ```

### Contribution Guidelines

- **Code Quality:** Follow Python PEP 8 standards
- **Documentation:** Update README for new features
- **Testing:** Test thoroughly before submitting
- **Security:** Ensure no vulnerabilities in contributed code

### Ideas for Contributions

- Additional WAF bypass techniques
- Performance optimizations
- New output formats (JSON, CSV)
- Integration with other security tools
- Enhanced error handling

---

## 👨‍💻 Author & Maintainer

**Suman Mandal**  
*Cybersecurity Student | Open Source Advocate | Community Builder*

- 🎓 **Education:** BCA Hons. in Cyber Security, Marwadi University
- 🔧 **Specializations:** OSINT, Linux Internals, Defensive Security, Malware Analysis
- 🌟 **Mission:** Building tech-for-good cybersecurity solutions and mentoring defenders
- 🎯 **Vision:** Secure the digital world through open-source tools and community empowerment

**Connect with me:**
- 📧 Email: [Coming Soon]
- 💼 LinkedIn: [Coming Soon]
- 🐙 GitHub: [@sumanmandal](https://github.com/sumanmandal)

---


# 🔭 Development Roadmap
- ### Version 1.1 (Planned)
  - **Multithreading support** for faster scanning
  - **Custom HTTP headers** and User-Agent rotation
  - **Rate limiting controls** for responsible scanning
  - **Improved error handling** and recovery

- ### Version 1.2 (Future)
  - **Recursive auto-discovery** with dynamic depth exploration
  - **Subdomain enumeration** integration
  - **Export capabilities** (CSV, JSON, PDF reports)
  - **Configuration file support** for saved settings


- ### Version 2.0 (Long-term Vision)
  - **GUI/Web interface**
  - **Advanced WAF bypass techniques**
  - **Integration with popular security frameworks**
  - **Cloud deployment options**
  - **Collaborative scanning features**

---

## 🙏 Acknowledgments

- **wafw00f team** for the excellent WAF detection library
- **Python requests library** maintainers
- **Cybersecurity community** for inspiration and feedback

---

## 📊 Project Statistics

- **Lines of Code:** ~500+ (modular and clean)
- **Dependencies:** Minimal (2 external libraries)
- **Python Version:** 3.8+ compatible
- **Platform Support:** Cross-platform (Windows, Linux, macOS)
- **License:** MIT (open source friendly)

---

*Last updated: May 2025 | Version 1.0 | Built with ❤️ for the cybersecurity community*
