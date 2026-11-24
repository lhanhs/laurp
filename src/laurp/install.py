import os
import subprocess
import tempfile
import core
from pathlib import Path

def install(packages: list):
    for package in packages:
        logfile = core.makelogfile()
        cmd = [
            "bash", "-c",
            f"git clone https://aur.archlinux.org/{package}.git && "
            f"cd {package} && makepkg -s --noconfirm"
        ]
        core.logsp(cmd, logfile)
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