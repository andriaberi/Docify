import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

def run(cmd: List[str], cwd: Optional[Path] = None, env: Optional[dict] = None,) -> Tuple[int, str, str]:
    p = subprocess.Popen(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    
    out, err = p.communicate()
    return p.returncode, out, err
