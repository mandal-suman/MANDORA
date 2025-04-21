# Async HTTP request handling

import requests
# import os
# import aiohttp, asyncio, aiofiles

site = "https://marwadiuniversity.ac.in"

try:
    with open('wordlists/wordlists.txt', 'r') as f:
        wordlists = f.read().splitlines()
        print("Wordlists loaded:")
        
        for wordlist in wordlists:
            try:
                response = requests.get(f"{site}{wordlist}")
                if response.status_code == 200:
                    print(f"[+] Successfully fetched {wordlist}")
                    with open('saved.txt', 'a') as saved_file:
                        saved_file.write(f"{site}{wordlist}\n")
                else:
                    print(f"[-] Failed to fetch {wordlist} with status code {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"[!] Error fetching {wordlist}: {e}")
except FileNotFoundError:
    print("[!] Error: 'wordlists/wordlists.txt' file not found.")
except Exception as e:
    print(f"[!] An unexpected error occurred: {e}")
            

