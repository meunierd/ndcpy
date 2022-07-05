import argparse
import rich
from . import NDC

from os.path import join

from rich import print
from rich.tree import Tree
from rich.text import Text


def ndc_list(args):
    ndc = NDC()
    tree = ndc_tree(ndc, args.image, args.path or "")
    print(tree)


def ndc_tree(ndc, image, path="", tree=None):
    if tree is None:
        tree = Tree(path)
    results = ndc.list(image, path)[1:]  # skip volume
    for name, _, name_type, _ in results:
        if name_type == NDC.DIR:
            branch = tree.add(name)
            ndc_tree(ndc, image, join(path, name), branch)
        else:
            tree.add(name)
    return tree


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
