# Work-in-progress remove function
# To-do: check if a package exists first.
# To-do: add a confirmation. Also applies to install function, but necessity is debatable. Proposed solution is to only ask for a confirmation if ran with root, because sudo authentication can be considered as a type of confirmation prompt.
import core
from pathlib import Path

def remove(packages: list):
    logfile = core.makelogfile()
    for package in packages:
        cmd = ["pacman", "-Rns", "--noconfirm", str(pkg)]
        core.logsp(cmd, logfile, 0)