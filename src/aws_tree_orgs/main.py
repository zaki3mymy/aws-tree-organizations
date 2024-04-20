from aws_tree_orgs.model import create_ou_tree
from aws_tree_orgs.view import to_markdown


def main():
    root_ou = create_ou_tree()
    print(to_markdown(root_ou))


if __name__ == "__main__":
    main()
