import os
import subprocess
import tempfile
import core
import shutil
from pathlib import Path

def install(packages: list):
    logfile = core.makelogfile()
    for package in packages:
        clonedir = Path(package)
        try:
            cmd = [
                "bash", "-c",
                f"git clone https://aur.archlinux.org/{package}.git && "
                f"cd {package} && makepkg -s --noconfirm"
            ]
            core.logsp(cmd, logfile, 0)
            pkg = next(Path(package).glob("*.pkg.tar.zst"), None)
            if not pkg:
                print(f"\033[1;31mE\033[0m: {package} build failed")
                continue
            cmd = ["pacman", "-U", "--noconfirm", str(pkg)]
            if os.geteuid() != 0:
                cmd.insert(0, "sudo")
            # Had to re-write logsp() here because of some design problems.
            with open(logfile, "a") as log:
                process = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
                process.wait()
            if process.returncode != 0:
                print(f"\033[1;31mE\033[0m: {package} installation failed")
        finally:
            if clonedir.exists():
                shutil.rmtree(clonedir, ignore_errors=True)