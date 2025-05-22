import requests
import os
import itertools
from urllib.parse import urlparse

class Mandora:
    def __init__(self, target_url, output_dir, wordlist_path='wordlists/wordlists.txt', max_depth=1):
        self.target_url = target_url.rstrip('/')
        self.wordlist_path = wordlist_path
        self.max_depth = min(max_depth, 4)
        self.wordlists = []
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

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

        depth_wise_urls = self.generate_paths()

        for depth, urls in depth_wise_urls.items():
            for _, url in urls:
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        print(f"[+] Found (depth {depth}): {url}")
                        self.save_result(depth, url)
                    else:
                        print(f"[-] Not Found ({response.status_code}): {url}")
                except requests.exceptions.RequestException as e:
                    print(f"[!] Request failed for {url}: {e}")

    def save_result(self, depth, url):
        filename = os.path.join(self.output_dir, f"depth_{depth}.txt")
        try:
            with open(filename, 'a') as f:
                f.write(f"{url}\n")
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
        mandora.scan()
        print(f"\n📁 Output saved in: {mandora.output_dir}")
    except FileNotFoundError as fe:
        print(fe)
    except Exception as e:
        print(f"[!] Unexpected error: {e}")