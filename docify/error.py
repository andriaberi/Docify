import sys

def handle_error(msg: str, term: bool = False):
    print("ERROR:", msg)
    if term:
        sys.exit()