# core.py provides core functionality for the helper. Intended for internal use only.
import shutil
import platform
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def makelogfile():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    logdir = Path.home() / ".local" / "share" / "laurp" / "logs"
    logdir.mkdir(parents=True, exist_ok=True)
    return logdir / f"{timestamp}.log"

def platformcheck() -> bool:
    info = platform.freedesktop_os_release()
    ids = {
        info.get("ID", "").lower(),
        *info.get("ID_LIKE", "").lower().split(),
    }
    return "arch" in ids and shutil.which("pacman") is not None

def logsp(command: list[str], logfile: str) -> int:
    with open(logfile, "a") as log:
        process = subprocess.Popen(
            command,
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True
        )
        exitcode = process.wait()
        print(f"Log file saved to {logfile}")
        return exitcode

def checkdeps():
    required = ["git", "makepkg", "pacman"]
    missing = [cmd for cmd in required if shutil.which(cmd) is None]
    return missing