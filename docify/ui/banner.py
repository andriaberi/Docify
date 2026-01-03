import os
import random
import shutil

BANNER = r"""
██████╗  ██████╗  ██████╗██╗███████╗██╗   ██╗
██╔══██╗██╔═══██╗██╔════╝██║██╔════╝╚██╗ ██╔╝
██║  ██║██║   ██║██║     ██║█████╗   ╚████╔╝ 
██║  ██║██║   ██║██║     ██║██╔══╝    ╚██╔╝  
██████╔╝╚██████╔╝╚██████╗██║██║        ██║   
╚═════╝  ╚═════╝  ╚═════╝╚═╝╚═╝        ╚═╝   
""".strip("\n")

GREETINGS = [
    "Reading your code so humans don’t have to.",
    "Turning code into documentation.",
    "Your codebase, explained."
]

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def center_lines(text: str, width: int) -> str:
    return "\n".join(line.center(width) for line in text.splitlines())

def print_banner() -> None:
    term_width = shutil.get_terminal_size((80, 20)).columns
    banner_width = min(term_width, 100)
    greeting = random.choice(GREETINGS)

    print()
    print(center_lines(BANNER, banner_width))
    print()
    print(greeting.center(banner_width))
    print(("-" * banner_width))
    print()
