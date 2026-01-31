import hashlib
import itertools
import os
from difflib import SequenceMatcher
from uuid import uuid4

import requests

class Mandora:
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/14.0 Safari/604.1.38",
    ]

    ACCEPT_LANGUAGES = [
        "en-US,en;q=0.9",
        "en-GB,en-US;q=0.9,en;q=0.8",
        "en-US,en;q=0.9,fr;q=0.7",
    ]

    DEFAULT_TIMEOUT = 10

    def __init__(self, target_url, output_dir, wordlist_path='wordlists/wordlists.txt', max_depth=1):
        self.target_url = target_url.rstrip('/')
        self.wordlist_path = wordlist_path
        self.max_depth = min(max_depth, 4)
        self.wordlists = []
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.session = requests.Session()
        self.user_agent_cycle = itertools.cycle(self.USER_AGENTS)
        self.language_cycle = itertools.cycle(self.ACCEPT_LANGUAGES)
        proxy_env = os.getenv("MANDORA_PROXIES", "").strip()
        self.proxy_pool = [proxy.strip() for proxy in proxy_env.split(",") if proxy.strip()]
        self.proxy_cycle = itertools.cycle(self.proxy_pool) if self.proxy_pool else None
        self.baseline_invalid = None
        self.stats = {
            "requests": 0,
            "valid": 0,
            "protected": 0,
            "redirect": 0,
            "soft_404": 0,
            "errors": 0,
        }

    def _build_headers(self):
        return {
            "User-Agent": next(self.user_agent_cycle),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": next(self.language_cycle),
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Referer": self.target_url,
        }

    def _pick_proxy(self):
        if not self.proxy_cycle:
            return None
        proxy = next(self.proxy_cycle)
        return {"http": proxy, "https": proxy}

    def _request(self, url):
        try:
            response = self.session.get(
                url,
                headers=self._build_headers(),
                proxies=self._pick_proxy(),
                timeout=self.DEFAULT_TIMEOUT,
                allow_redirects=True,
            )
            return response
        except requests.exceptions.RequestException as exc:
            print(f"[!] Request failed for {url}: {exc}")
            return None

    def _extract_signature(self, response):
        if response is None:
            return None
        text = response.text
        sample = text[:2000].strip()
        digest = hashlib.sha1(sample.encode("utf-8", errors="ignore")).hexdigest()
        return {
            "status": response.status_code,
            "url": response.url.rstrip('/'),
            "length": len(text),
            "hash": digest,
            "sample": sample,
        }

    def _looks_like_soft_404(self, response):
        if not self.baseline_invalid:
            return False
        candidate = self._extract_signature(response)
        if not candidate:
            return False
        if candidate["hash"] == self.baseline_invalid["hash"]:
            return True
        length_base = self.baseline_invalid["length"] or 1
        length_candidate = candidate["length"] or 1
        length_similarity = 1 - (abs(length_base - length_candidate) / max(length_base, length_candidate))
        if length_similarity > 0.98:
            return True
        ratio = SequenceMatcher(None, self.baseline_invalid["sample"], candidate["sample"]).ratio()
        return ratio > 0.94

    def _prepare_baseline(self):
        probe_url = f"{self.target_url}/mandora-probe-{uuid4().hex}"
        invalid_response = self._request(probe_url)
        if invalid_response is not None:
            self.baseline_invalid = self._extract_signature(invalid_response)

    def load_wordlist(self):
        if not os.path.exists(self.wordlist_path):
            raise FileNotFoundError(f"[!] Wordlist not found at {self.wordlist_path}")
        with open(self.wordlist_path, 'r') as file:
            self.wordlists = file.read().splitlines()
        print("✅ Wordlists loaded successfully")

    def generate_paths(self):
        depth_paths = {}
        for depth in range(1, self.max_depth + 1):
            paths = []
            for combo in itertools.product(self.wordlists, repeat=depth):
                path = "/".join(combo)
                full_url = f"{self.target_url}/{path}"
                paths.append((depth, full_url))
            depth_paths[depth] = paths
        return depth_paths

    def scan(self):
        if not self.wordlists:
            print("[!] No wordlists loaded. Exiting...")
            return

        self._prepare_baseline()
        depth_wise_urls = self.generate_paths()

        for depth, urls in depth_wise_urls.items():
            for _, url in urls:
                try:
                    self.stats["requests"] += 1
                    response = self._request(url)
                    if response is None:
                        continue
                    classification, info = self._classify_response(response, url)
                except KeyboardInterrupt:
                    raise
                except Exception as exc:
                    self.stats["errors"] += 1
                    print(f"[!] Unexpected error while processing {url}: {exc}")
                    continue

                if response is None:
                    continue
                if classification == "valid":
                    self.stats["valid"] += 1
                    print(f"[+] Found (depth {depth}): {url} [status {response.status_code}]")
                    self.save_result(depth, url, response.status_code, info)
                elif classification == "protected":
                    self.stats["protected"] += 1
                    print(f"[+] Protected resource (depth {depth}): {url} [status {response.status_code}]")
                    self.save_result(depth, url, response.status_code, info)
                elif classification == "redirect":
                    self.stats["redirect"] += 1
                    print(f"[~] Redirected to {info} from {url}")
                elif classification == "soft-404":
                    self.stats["soft_404"] += 1
                    print(f"[-] Soft 404 detected: {url}")
                else:
                    print(f"[-] Not Found ({response.status_code}): {url}")

    def summary(self):
        if not self.stats["requests"]:
            return "No requests were issued."
        lines = [
            f"Total requests: {self.stats['requests']}",
            f"Valid hits: {self.stats['valid']}",
            f"Protected hits: {self.stats['protected']}",
            f"Redirects skipped: {self.stats['redirect']}",
            f"Soft 404 filtered: {self.stats['soft_404']}",
            f"Processing errors: {self.stats['errors']}",
        ]
        return "\n".join(lines)

    def _classify_response(self, response, requested_url):
        normalized_requested = requested_url.rstrip('/')
        normalized_final = response.url.rstrip('/')
        redirected = bool(response.history) and normalized_final != normalized_requested

        if redirected:
            return "redirect", response.url

        if response.status_code in (401, 403):
            return "protected", "Access controlled"

        if response.status_code == 200:
            if self._looks_like_soft_404(response):
                return "soft-404", "Content matches baseline invalid response"
            return "valid", "OK"

        if response.status_code in (301, 302, 307, 308):
            return "redirect", response.headers.get("Location", "")

        return "invalid", response.status_code

    def save_result(self, depth, url, status_code, note):
        filename = os.path.join(self.output_dir, f"depth_{depth}.txt")
        try:
            with open(filename, 'a') as f:
                f.write(f"{url}\tstatus={status_code}\t{note}\n")
        except Exception as e:
            print(f"[!] Failed to write to file {filename}: {e}")

def start_scan(target_url, output_folder):
    try:
        depth = int(input("Enter max depth (1 to 4): ").strip())
        if depth < 1 or depth > 4:
            raise ValueError("Depth must be between 1 and 4.")
    except ValueError as ve:
        print(f"[!] Invalid depth value: {ve}")
        return

    mandora = Mandora(target_url=target_url, output_dir=output_folder, max_depth=depth)

    try:
        mandora.load_wordlist()
        interrupted = False
        try:
            mandora.scan()
        except KeyboardInterrupt:
            interrupted = True
            print("\n[!] Scan interrupted by user. Partial results preserved.")
        finally:
            summary_text = mandora.summary()
            if summary_text:
                print("\n--- Scan Summary ---")
                print(summary_text)
        if not interrupted:
            print(f"\n📁 Output saved in: {mandora.output_dir}")
        return mandora.stats
    except FileNotFoundError as fe:
        print(fe)
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
    return mandora.stats