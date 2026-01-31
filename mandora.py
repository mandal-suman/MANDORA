import os
from urllib.parse import urlparse
from core.waf_detector import detect_waf
from core.scanner import start_scan

def sanitize_url_to_folder(url):
    parsed = urlparse(url)
    candidate = parsed.netloc or parsed.path
    sanitized = []
    for char in candidate:
        if char.isalnum() or char in {"_", "-"}:
            sanitized.append(char)
        elif char in {".", ":"}:
            sanitized.append("_")
        else:
            sanitized.append("-")
    sanitized_value = "".join(sanitized).strip("-_")
    if not sanitized_value:
        sanitized_value = "target"
    return sanitized_value


def ensure_scheme(url):
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}".strip()
        parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http and https schemes are supported.")
    if not parsed.netloc:
        raise ValueError("Target URL appears invalid.")
    return url

def main():
    print("=== MANDORA: Directory Bruteforcer with WAF Detection ===")
    try:
        raw_target = input("\U0001F310 Enter target site (e.g., https://example.com): ").strip()
        if not raw_target:
            print("[!] Target URL is required. Aborting.")
            return
        target_site = ensure_scheme(raw_target)

        folder_name = sanitize_url_to_folder(target_site)
        output_folder = os.path.join("output", folder_name)

        # Step 1: Detect WAF
        detections = detect_waf(target_site, output_folder)
        if detections:
            print(f"Detected {len(detections)} WAF signal(s). Details saved to output directory.")

        # Step 2: Start Bruteforcing
        start_scan(target_site, output_folder)

    except KeyboardInterrupt:
        print("\n[!] Execution interrupted by user.")
    except ValueError as ve:
        print(f"[!] {ve}")
    except Exception as exc:
        print(f"[!] Unexpected error: {exc}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Terminated by user.")