import sys

def handle(msg: str, exit_program: bool = False):
    print("ERROR:", msg)
    if exit_program:
        sys.exit()