from colorama import Fore, Back, Style

qwoqLab_description = "qwoqLab is automated reversing tool for CSAPP bomblab."


def print_title() -> None:
    title = r"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ qwoqLab - automated reverse of bomblab      $$\                $$\        ┃
┃                                             $$ |               $$ |       ┃
┃  $$$$$$\  $$\  $$\  $$\  $$$$$$\   $$$$$$\  $$ |      $$$$$$\  $$$$$$$\   ┃
┃ $$  __$$\ $$ | $$ | $$ |$$  __$$\ $$  __$$\ $$ |      \____$$\ $$  __$$\  ┃
┃ $$ /  $$ |$$ | $$ | $$ |$$ /  $$ |$$ /  $$ |$$ |      $$$$$$$ |$$ |  $$ | ┃
┃ $$ |  $$ |$$ | $$ | $$ |$$ |  $$ |$$ |  $$ |$$ |     $$  __$$ |$$ |  $$ | ┃
┃ \$$$$$$$ |\$$$$$\$$$$  |\$$$$$$  |\$$$$$$$ |$$$$$$$$\\$$$$$$$ |$$$$$$$  | ┃
┃  \____$$ | \_____\____/  \______/  \____$$ |\________|\_______|\_______/  ┃
┃       $$ |                              $$ |                              ┃
┃       $$ |                              $$ |                              ┃
┃       \__|                              \__|                              ┃
┃                                       Bomblab automated reverse by Aplace ┃
┃                                                special thanks to n1net4il ┃
┃                                                                  minsusun ┃                    
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

    for ch in title:
        if ch in ["|", "\\", "/", "_", " "]:
            print(f"{Fore.LIGHTBLACK_EX}{ch}{Style.RESET_ALL}", end="")
        elif ch == "$":
            print(f"{Fore.CYAN}{ch}{Style.RESET_ALL}", end="")
        else:
            print(ch, end="")
