# aws-tree-organizations

This is a simple tool to visualize the AWS Organizations structure in a tree format.

For example, if your AWS Organizations hierarchy looks like the diagram below:
![image](https://github.com/zaki3mymy/aws-tree-organizations/assets/91773180/f6786031-5feb-4628-b6a4-a103c6a5e986)

The result is the simplified diagram below. Above the arrow are SCPs applied to the OU or account.
```mermaid
flowchart LR
    r-xxxx[(Root)]
    r-xxxx --FullAWSAccess
DenyLeaveOrganizations--> ou-xxxx-12345678 & ou-xxxx-22345678
    123456789012[root-account
    123456789012]
    123456789012 -- FullAWSAccess --> 123456789012
    r-xxxx --FullAWSAccess
DenyLeaveOrganizations--> 123456789012

    ou-xxxx-12345678[(prod)]
    223456789012[projectA-prd
    223456789012]
    223456789012 -- FullAWSAccess --> 223456789012
    ou-xxxx-12345678 --FullAWSAccess--> 223456789012

    ou-xxxx-22345678[(dev)]
    323456789012[projectA-dev
    323456789012]
    323456789012 -- FullAWSAccess --> 323456789012
    423456789012[projectB-dev
    423456789012]
    423456789012 -- FullAWSAccess --> 423456789012
    523456789012[projectC-dev
    523456789012]
    523456789012 -- FullAWSAccess --> 523456789012
    ou-xxxx-22345678 --FullAWSAccess--> 323456789012 & 423456789012 & 523456789012
```

This diagram is written by mermaid(flowchart). So, you can use it in your markdown file.


## Requirements

- Python 3.6+
- [rye](https://rye-up.com/)


## Installation

```bash
rye build
rye install dist/aws-tree-orgs-x.y.z.tar.gz
```


## Usage

```bash
aws-tree-orgs

# or specify a profile
aws-tree-orgs --profile <profile_name>
```
