import core
import install
import sys
import argparse
import os

def main():
            parser = argparse.ArgumentParser(description="laurp — Minimalist, uncomplicated AUR helper")
            subparsers = parser.add_subparsers(dest="action", required=True)
            installparser = subparsers.add_parser("install", help="Install packages")
            installparser.add_argument("packages", nargs="+", help="Packages to install")
            args = parser.parse_args()
            if args.action == "install":
                install.install(args.packages)


def entry():
    if core.platformcheck():
        missing = core.checkdeps()
        if missing:
            print(f"\033[1;31mE\033[0m: {", ".join(missing)} not found.")
            sys.exit(1)
        else:
            main()

    else:
        print(f"\033[1;31mE\033[0m: This machine is on an unsupported platform")
        sys.exit(1)

if __name__ == "__main__":
    entry()