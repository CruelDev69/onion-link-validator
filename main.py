# safe_onion_finder.py
# Purpose: Legality-first onion finder that filters out illegal/risky categories.
# Jurisdiction note (Pakistan/PECA 2016): This tool is designed to AVOID indexing/promoting illegal content.
# It must only be used for research/educational purposes with lawful content.

import requests
import re
from colorama import Fore, Style
import os
from messages import log

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/110.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

AHMIA_URLS = [
    "https://ahmia.fi",
    "http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion"
]

HIDDEN_WIKI_MIRRORS = [
    "http://bfbzii56g2brpsg3a6hng45noo4lnby3ux5sgvpd53dyzpu3cre35ryd.onion/",
    "https://thehiddenwiki.org"
]

TORCH_URL = "http://searxingux6na3djgdrcfwutafxmmagerhbieihsgu7sgmjee3u777yd.onion/"

ONION_REGEX = re.compile(r"(?:http://)?[a-z2-7]{56}\.onion")

BLOCKED_KEYWORDS = {
    # drugs
    "drug", "narcotic", "coke", "cocaine", "heroin", "meth", "lsd", "weed", "cannabis",
    # weapons
    "gun", "weapon", "firearm", "explosive",
    # fraud & crime services
    "carding", "cvv", "fullz", "skimmer", "counterfeit", "fake id", "forged id",
    "hack", "hacker for hire", "ransomware", "malware", "botnet", "ddos", "exploit",
    # CSAM/obscene (zero tolerance)
    "cp", "child", "lolita", "sex",
    # terror / extremism
    "isis", "terror", "extremist",
    # other obvious banned markets/services
    "hitman", "assassin", "murder for hire", "stolen data", "leakbase",
}

# ------------------------------
# Search Functions
# ------------------------------

def is_safe_query(query: str) -> bool:
    q = query.lower()
    return not any(bad_word in q for bad_word in BLOCKED_KEYWORDS)

def search_ahmia(query):
    onions = set()
    if not is_safe_query(query):
        print(log("Query contains illegal or blocked keywords.", "info"))
        return []
    for base in AHMIA_URLS:
        try:
            r = requests.get(f"{base}/search/?q={query}", headers=HEADERS, proxies=proxies, timeout=20)
            r.raise_for_status()
            onions |= set(ONION_REGEX.findall(r.text))
        except Exception as e:
            print(log(f"Error searching Ahmia ({base}): {e}", "error"))
    return list(onions)


def scrape_hidden_wiki(query):
    onions = set()
    if not is_safe_query(query):
        print(log("Query contains illegal or blocked keywords.", "info"))
        return []
    for base in HIDDEN_WIKI_MIRRORS:
        try:
            r = requests.get(base, headers=HEADERS, proxies=proxies, timeout=20)
            r.raise_for_status()
            onions |= set(ONION_REGEX.findall(r.text))
        except Exception as e:
            print(log(f"Error scraping Hidden Wiki ({base}): {e}", "error"))
    return list(onions)


def search_torch(query):
    onions = set()
    if not is_safe_query(query):
        print(log("Query contains illegal or blocked keywords.", "info"))
        return []
    try:
        r = requests.get(f"{TORCH_URL}/search?q={query}", headers=HEADERS, proxies=proxies, timeout=20)
        r.raise_for_status()
        onions |= set(ONION_REGEX.findall(r.text))
    except Exception as e:
        print(log(f"Error searching Torch: {e}", "error"))
    return list(onions)

# ------------------------------
# Onion Checker
# ------------------------------

def check_onion(url):
    if not url.startswith("http://"):
        url = "http://" + url
    try:
        r = requests.get(url, headers=HEADERS, proxies=proxies, timeout=15)
        return r.status_code == 200
    except Exception:
        return False

# ------------------------------
# Menu
# ------------------------------

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_banner():
    banner = f"""
{Fore.GREEN}{Style.BRIGHT}
.-,--.     ,.   .-,--. ,-, ,   .---. .  . `.--- ,-,-.   ,-_/ ,--,--'`.--- 
' |   \   / |    `|__/  '|/    \___  |  |  |__  ` | |   '  | `- |    |__  
, |   /  /~~|-.   | \    |\        \ |  | ,|      | |-. .- |  , |   ,|    
`-^--' ,'   `-' `-'  `  ,' `   `---' `--| `^---  ,' `-' `--'  `-'   `^--- 
                                     .- |                                 
                                     `--'                                 
       by: Ahad#3257/CruelDev69
       repo: https://github.com/CruelDev69/onion-link-validator
       disclaimer: 
       - This tool applies strict keyword-based blocking to avoid illegal content.
       - It is provided for research/educational and privacy-awareness purposes ONLY.
       - Do not use this tool to seek or access illegal content. You are responsible for your use.
       - In Pakistan (PECA 2016), facilitating access to illegal content/services can be a criminal offense.
{Style.RESET_ALL}
"""
    print(banner)


def show_menu():
    print(log("===================================", "info"))
    print(log("[1] Ahmia", "info"))
    print(log("[2] Hidden Wiki", "info"))
    print(log("[3] Torch", "info"))
    print(log("===================================", "info"))
    choice = input(Fore.GREEN + "Select search engine (1-3): " + Fore.WHITE).strip()
    return choice

# ------------------------------
# Main
# ------------------------------

if __name__ == "__main__":
    clear_screen()
    show_banner()

    choice = show_menu()
    keyword = input(Fore.MAGENTA + "Enter search keyword: " + Fore.WHITE).strip()

    onions = []
    if choice == "1":
        print(log(f"Searching Ahmia for '{keyword}'...", "info"))
        onions = search_ahmia(keyword)
    elif choice == "2":
        print(log("Scraping Hidden Wiki...", "info"))
        onions = scrape_hidden_wiki(keyword)
    elif choice == "3":
        print(log(f"Searching Torch for '{keyword}'...", "info"))
        onions = search_torch(keyword)
    else:
        print(log("Invalid choice", "error"))
        exit()

    print(log(f"Found {len(onions)} potential onion addresses.", "success"))

    found = []
    for onion in onions:
        print(log(f"Checking {onion} ...", "info"))
        if check_onion(onion):
            print(log(f"Live: {onion}", "success"))
            found.append(onion)
            with open("found_onions.txt", "a", encoding="utf-8") as f:
                f.write(onion + "\n")

    print(log("===================================", "info"))
    print(log("Scan Complete. Live onions:", "success"))
    for f in found:
        print(log(" -> " + f, "success"))
    print(log("===================================", "info"))
