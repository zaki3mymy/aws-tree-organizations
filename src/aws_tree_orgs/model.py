import json
from typing import NamedTuple

import boto3


class Account(NamedTuple):
    id: str
    name: str
    parent_id: str
    scp: list[str]

    def add_scp(self, scp: str):
        self.scp.append(scp)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
            "scp": self.scp,
        }


class OrganizationalUnit(NamedTuple):
    id: str
    name: str
    parent_id: str
    ous: list  # List of child(OrganizationalUnit)
    accounts: list  # List of child(Account)
    scp: list[str]

    def add_child_ou(self, child: "OrganizationalUnit"):
        self.ous.append(child)

    def add_child_account(self, child: Account):
        self.accounts.append(child)

    def add_scp(self, scp: str):
        self.scp.append(scp)

    def __eq__(self, other: "OrganizationalUnit"):
        return (
            self.id == other.id
            and self.name == other.name
            and self.parent_id == other.parent_id
            and self.ous == other.ous
            and self.accounts == other.accounts
        )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
            "ous": [ou.to_dict() for ou in self.ous],
            "accounts": [account.to_dict() for account in self.accounts],
            "scp": self.scp,
        }

    def to_json(self, indent=None):
        return json.dumps(self.to_dict(), indent=indent)


class Organization(NamedTuple):
    root: OrganizationalUnit
    ou_dict: dict[str, OrganizationalUnit]

    def add_ou(self, ou: OrganizationalUnit):
        self.ou_dict[ou.id] = ou

    def get_ou(self, ou_id: str):
        return self.ou_dict[ou_id]


def _list_policies_for_target(client: boto3.client, target_id: str):
    policies = client.list_policies_for_target(
        TargetId=target_id, Filter="SERVICE_CONTROL_POLICY"
    )["Policies"]
    # ポリシー名のリストを返す
    return sorted([policy["Name"] for policy in policies])


def _create_ou(
    parent_ou: OrganizationalUnit, client: boto3.client, organization: Organization
):
    # 再帰的にOUの階層構造を作成
    ous = client.list_organizational_units_for_parent(ParentId=parent_ou.id)
    for ou in ous["OrganizationalUnits"]:
        ou_id = ou["Id"]
        ou_name = ou["Name"]
        policies = _list_policies_for_target(client, ou_id)

        ou_acc = OrganizationalUnit(ou_id, ou_name, parent_ou.id, [], [], policies)
        organization.add_ou(ou_acc)
        ou_acc = _create_ou(ou_acc, client, organization)
        parent_ou.add_child_ou(ou_acc)
    return parent_ou


def _add_account_to_ou(account_id: str, org: Organization, client: boto3.client):
    account = client.describe_account(AccountId=account_id)["Account"]
    parent = client.list_parents(ChildId=account_id)["Parents"][0]

    parent_id = parent["Id"]
    policies = _list_policies_for_target(client, account_id)
    acc = Account(account_id, account["Name"], parent_id, policies)
    ou = org.get_ou(parent_id)
    ou.add_child_account(acc)


def create_ou_tree() -> OrganizationalUnit:
    client = boto3.client("organizations")
    root = client.list_roots()["Roots"][0]

    policies = _list_policies_for_target(client, root["Id"])
    root_ou = OrganizationalUnit(root["Id"], "Root", None, [], [], policies)
    organization: Organization = Organization(root_ou, {})
    organization.add_ou(root_ou)

    # 再帰的にOUの階層構造を作成
    root_ou = _create_ou(root_ou, client, organization)

    # アカウントのリストを取得
    accounts = client.list_accounts()
    for account in accounts["Accounts"]:
        account_id = account["Id"]
        # アカウントをOUに紐づける
        _add_account_to_ou(account_id, organization, client)

    return root_ou
