# core.py provides core functionality for the helper and is intended for internal use only.
import requests

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

def logsp(command: list[str], logfile: str, verbose=1) -> int:
    with open(logfile, "a") as log:
        process = subprocess.Popen(
            command,
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True
        )
        exitcode = process.wait()
        if verbose:
            print(f"Log file saved to {logfile}")
        return exitcode

def checkdeps():
    required = ["git", "makepkg", "pacman"]
    missing = [cmd for cmd in required if shutil.which(cmd) is None]
    return missing

# NETWORKING
# For now, networking only accepts package strings. List handling will be added later.
def networking(action: str, package: str):
    # Actions: search, info
    url = f"https://aur.archlinux.org/rpc/v5/{action}/" + package
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["results"]

