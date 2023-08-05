"""Console script for proma"""

# import argparse
import sys

import proma
from proma.proma import (
    create,
    test,
    build,
    install,
    develop,
    doc,
    clean,
    upload,
    init,
    uninstall,
    print_help,
)


def main():
    action = sys.argv[1]
    param = sys.argv[2:]
    # parser = argparse.ArgumentParser()
    # parser.add_argument("action", type=str)
    # parser.add_argument("_", nargs="*")
    # args = parser.parse_args()

    # param = args._

    if action == "--version":
        print("proma v" + proma.__version__)
    elif action == "help":
        print_help()
    elif action == "create":
        create(param[0])
    elif action == "test":
        test(param)
    elif action == "build":
        build(param)
    elif action == "install":
        install(param)
    elif action == "uninstall":
        uninstall(param)
    elif action == "init":
        init(param)
    elif action == "develop":
        develop(param)
    elif action == "doc":
        doc(param)
    elif action == "clean":
        clean(param)
    elif action == "upload":
        upload(param)
    else:
        print("[ERREUR]Action inconnue : '%s'" % action)

    return 0


if __name__ == "__main__":
    sys.exit(main())
