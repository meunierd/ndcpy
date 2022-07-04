import argparse
import rich
from . import NDC

from rich import print
from rich.tree import Tree
from rich.text import Text


def ndc_list(args):
    ndc = NDC()
    tree = Tree("dir")
    for path, dirs, files in ndc.walk(image=args.image):
        for directory in dirs:
            tree.add(directory)


def parse_args():
    parser = argparse.ArgumentParser(prog="ndcpy")
    subparsers = parser.add_subparsers(help="sub-command help")
    list_cmd = subparsers.add_parser("list")
    list_cmd.add_argument("image", type=str, help="bar help")
    list_cmd.add_argument("path", type=str, help="bar help", nargs="*")
    list_cmd.set_defaults(func=ndc_list)
    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
