# colors.py
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

def log(message: str, level: str = "info") -> str:
    """
    Returns a timestamped, colored log string with hacker-style tags.
    
    Levels:
      success -> [+] (green)
      info    -> [*] (cyan)
      warn    -> [!] (yellow)
      error   -> [-] (red)
    """
    level = level.lower()
    time_tag = datetime.now().strftime("%H:%M:%S")

    if level == "success":
        tag = Fore.GREEN + "[+]" + Style.RESET_ALL
    elif level == "info":
        tag = Fore.CYAN + "[*]" + Style.RESET_ALL
    elif level == "warn":
        tag = Fore.YELLOW + "[!]" + Style.RESET_ALL
    elif level == "error":
        tag = Fore.RED + "[-]" + Style.RESET_ALL
    else:
        tag = Fore.WHITE + "[?]" + Style.RESET_ALL

    return f"{Fore.MAGENTA}[{time_tag}]{Style.RESET_ALL} {tag} {message}"