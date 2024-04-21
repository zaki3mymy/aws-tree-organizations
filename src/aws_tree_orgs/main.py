import argparse

from aws_tree_orgs.model import create_ou_tree
from aws_tree_orgs.view import to_markdown


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--profile")

    args = parser.parse_args()
    profile = args.profile

    root_ou = create_ou_tree(profile)
    print(to_markdown(root_ou))


if __name__ == "__main__":
    main()
