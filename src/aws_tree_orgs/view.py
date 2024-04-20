from aws_tree_orgs.model import Account, OrganizationalUnit

indent = "    "


def _write_account(account: Account):
    lines = []
    lines.append(f"{indent}{account.id}[{account.name}\n{indent}{account.id}]")
    if account.scp:
        arrow = "-- {} -->".format("\n".join(account.scp))
        lines.append(f"{indent}{account.id} {arrow} {account.id}")
    return lines


def _write_ou(ou: OrganizationalUnit):
    lines = []
    lines.append(f"{indent}{ou.id}[({ou.name})]")

    arrow = "-->"
    if ou.scp:
        arrow = "--{}-->".format("\n".join(ou.scp))

    if ou.ous:
        lines.append(f"{indent}{ou.id} {arrow} {' & '.join([child.id for child in ou.ous])}")
    if ou.accounts:
        for acc in ou.accounts:
            lines.extend(_write_account(acc))
        lines.append(f"{indent}{ou.id} {arrow} {' & '.join([child.id for child in ou.accounts])}")

    lines.append("")
    for child in ou.ous:
        lines.extend(_write_ou(child))

    return lines


def to_markdown(ou: OrganizationalUnit):
    lines = [
        "# Organizations Tree",
        "",
        "```mermaid",
        "flowchart LR",
    ]

    lines.extend(_write_ou(ou))

    lines.append("```")

    return "\n".join(lines)
