import sys
import logging
import awsinputs
import organizations
import json
from deepdiff import DeepDiff
from botocore.exceptions import ClientError


class organizationstasks():

    def __init__(self):
        pass

    def create_organization(self, session, config):
        org_client = organizations.organizations(session)
        for org, values in config["resources"]["organizations"].iteritems():
            try:
                org_client.create_organization(
                    featureset=values['featureset']
                )
            except ClientError as err:
                logging.warn(err)
                sys.exit(1)

    def upsert_org_account(self, session, config, noop=True, logoutput=None):
        org_client = organizations.organizations(session)
        aws_accounts = org_client.list_accounts()
        config_accounts = config["resources"]["accounts"]

        if logoutput:
            print json.dumps(aws_accounts, default=str, sort_keys=True, indent=4, separators=(',', ': '))
            print json.dumps(config_accounts, default=str, sort_keys=True, indent=4, separators=(',', ': '))

        new_accounts = [x for x in config_accounts.items() if x[1]["Name"] not in (y["Name"] for y in aws_accounts)]

        if noop:
            print json.dumps(new_accounts, default=str, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            for account in new_accounts:
                print account[1]
                try:
                    org_client.create_account(
                        email=account[1]['Email'],
                        accountname=account[1]['Name'],
                        rolename=account[1]['Rolename'],
                        iamuseraccess=account[1]['IamUserAccess']
                    )
                except ClientError as err:
                    logging.warn(err)
                    sys.exit(1)

    def upsert_policy(self, session, config):
        org_client = organizations.organizations(session)
        for policy, values in config["resources"]["scp"].iteritems():
            policy = self.get_policy_by_name(session=session, name=values['name'])
            if awsinputs.IsSCP(policy['Id']):
                try:
                    org_client.update_policy(
                        policyid=policy['Id'],
                        name=values['name'],
                        description=values['description'],
                        content=values['content']
                    )
                except ClientError as err:
                    logging.warn(err)
                    sys.exit(1)
            else:
                try:
                    org_client.create_policy(
                        name=values['name'],
                        description=values['description'],
                        content=values['content'],
                        orgtype=values['orgtype']
                    )
                except ClientError as err:
                    logging.warn(err)
                    sys.exit(1)

    def upsert_org_unit(self, session, config, logoutput=None):
        # org_client = organizations.organizations(session)
        config_org_tree = {'Name': 'Root', 'Children': []}
        for org in config["resources"]["org_units"].iteritems():
            config_org_tree['Children'].append(self.config_organization_tree(org))
        if logoutput:
            print json.dumps(config_org_tree, default=str, sort_keys=True, indent=4, separators=(',', ': '))
        # master_org_tree = self.organization_tree(session=session)
        master_org_tree = {
            "Children": [
                {
                    "Children": [
                        {
                            "Children": [],
                            "Name": "IAM"
                        },
                        {
                            "Children": [],
                            "Name": "Build"
                        },
                        {
                            "Children": [
                                {
                                    "Children": [],
                                    "Name": "Prod"
                                },
                                {
                                    "Children": [],
                                    "Name": "Non Prod"
                                }
                            ],
                            "Name": "Run"
                        }
                    ],
                    "Name": "Stockland Core"
                },
                {
                    "Children": [
                        {
                            "Children": [],
                            "Name": "IAM"
                        },
                        {
                            "Children": [],
                            "Name": "Build"
                        },
                        {
                            "Children": [],
                            "Name": "Run"
                        }
                    ],
                    "Name": "Kablamo Core"
                }
            ],
            "Name": "Root"
        }
        compare_list = self.compare_org_tree(config=config_org_tree, master=master_org_tree)
        print json.dumps(compare_list, default=str, sort_keys=True, indent=4, separators=(',', ': '))

    def get_roots(self, session):
        org_client = organizations.organizations(session)
        roots = org_client.list_roots()

        return roots

    def get_account_status(self, session, accountid):
        org_client = organizations.organizations(session)
        accounts = org_client.list_accounts()
        discreet_account = [x for x in accounts if x['Id'] == accountid]

        return discreet_account['Status']

    def get_account_id(self, session, name):
        org_client = organizations.organizations(session)
        accounts = org_client.list_accounts()
        discreet_account = [x for x in accounts if x['Name'] == name]

        return discreet_account['Id']

    def get_policy_by_name(self, session, name):
        org_client = organizations.organizations(session)
        policies = org_client.list_policies()
        discreet_policy = [x for x in policies if x['Name'] == name]

        return discreet_policy

    def config_organization_tree(self, config):
        if isinstance(config, dict):
            for org, children in config.iteritems():
                organization_tree = {'Name': org, 'Children': []}
                if children is not None:
                    for child in children.iteritems():
                        organization_tree['Children'].append(self.config_organization_tree(config=child))
        elif isinstance(config, tuple):
            organization_tree = {'Name': config[0], 'Children': []}
            if isinstance(config[1], dict):
                for child in config[1].iteritems():
                    organization_tree['Children'].append(self.config_organization_tree(config=child))
        else:
            organization_tree = {'Name': config, 'Children': []}
        return organization_tree

    def organization_tree(self, session, depth=None, logoutput=None):
        organization_tree = {}
        org_client = organizations.organizations(session)
        for root in self.get_roots(session=session):
            organization_tree = self.buildorgtree(org_id=root['Id'], org_client=org_client, depth=depth, count=0)

        if logoutput:
            print json.dumps(organization_tree, default=str, sort_keys=True, indent=4, separators=(',', ': '))

        return organization_tree

    def buildorgtree(self, org_id, org_client, count, depth=None, full_info=False):
        if depth and int(count) > int(depth):
            return {}
        else:
            count += 1
            if full_info:
                child_set = {'Id': org_id, 'Children': [], 'Accounts': []}
            else:
                child_set = {'Children': []}
            org_details = {}

            if awsinputs.IsOU(org_id):
                org_details = org_client.describe_organization_unit(orgunitid=org_id)
            else:
                org_details['Name'] = "Root"
            child_set['Name'] = org_details['Name']
            if full_info:
                accounts = org_client.list_children(parentid=org_id, childtype='ACCOUNT')
                for account in accounts:
                    child_set['Accounts'].append(org_client.describe_account(accountid=account['Id']))
            children = org_client.list_children(parentid=org_id, childtype='ORGANIZATIONAL_UNIT')
            for child in children:
                child_set['Children'].append(self.buildorgtree(org_id=child['Id'], org_client=org_client, depth=depth, count=count))

        return child_set

    def compare_org_tree(self, config, master):
        delta = DeepDiff(config, master, ignore_order=True, indent=2)
        print json.dumps(DeepDiff(config, master, ignore_order=True, indent=2), sort_keys=True, indent=4, separators=(',', ': '))
        print delta
        new_org = [x for x in delta['iterable_item_added'] if x not in delta['iterable_item_removed']]
        print new_org
        # print json.dumps(DeepDiff(config, master, ignore_order=True),
        #     sort_keys=True, indent=4, separators=(',', ': '))
        # # print {k: v for k, v in config.items() if master[k] == v}
