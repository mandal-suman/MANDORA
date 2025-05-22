import os
from urllib.parse import urlparse
from core.waf_detector import detect_waf
from core.scanner import start_scan

def sanitize_url_to_folder(url):
    parsed = urlparse(url)
    return parsed.netloc.replace(".", "_")

def main():
    print("=== MANDORA: Directory Bruteforcer with WAF Detection ===")
    target_site = input("\U0001F310 Enter target site (e.g., https://example.com): ").strip()

    folder_name = sanitize_url_to_folder(target_site)
    output_folder = os.path.join("output", folder_name)

    # Step 1: Detect WAF
    detect_waf(target_site, output_folder)

    # Step 2: Start Bruteforcing
    start_scan(target_site, output_folder)

if __name__ == "__main__":
    main()