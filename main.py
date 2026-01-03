from pathlib import Path
from docify import run

BASE_DIR = Path(__file__).resolve().parent
WORK_DIR = BASE_DIR / '.work'
RESULTS_DIR = BASE_DIR / 'results'

if __name__ == "__main__":
    run(WORK_DIR, RESULTS_DIR)
