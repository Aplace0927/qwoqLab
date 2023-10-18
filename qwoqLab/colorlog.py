from colorama.ansi import AnsiFore, AnsiBack, AnsiStyle
from colorama import Fore, Back, Style

from typing import Any


def log(
    style: list[AnsiFore | AnsiBack | AnsiStyle], icon: str, txt: str, info: str = ""
) -> None:
    print("".join(style), end="")
    print(icon, end=f"{Style.RESET_ALL} ")
    print(txt, end="\t")
    print(f"{Fore.LIGHTBLACK_EX}{info}{Style.RESET_ALL}")
