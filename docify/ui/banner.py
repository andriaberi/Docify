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

def _center_lines(text: str, width: int) -> str:
    return "\n".join(line.center(width) for line in text.splitlines())

def print_banner() -> None:
    term_width = shutil.get_terminal_size((80, 20)).columns
    greeting = random.choice(GREETINGS)

    print()
    print(_center_lines(BANNER, min(term_width, 120)))
    print()
    print(greeting.center(min(term_width, 120)))
    print(("-" * min(term_width, 120)))
    print()
