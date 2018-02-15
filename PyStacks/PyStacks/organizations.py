
class organizations:

    def __init__(self, session):
        self.org_client = session.client('organizations')

    def create_account(self, email, accountname, rolename, iamuseraccess='DENY'):
        self.org_client.create_account(
            Email=email,
            AccountName=accountname,
            RoleName=rolename,
            IamUserAccessToBilling=iamuseraccess
        )

    def create_organization(self, featureset):
        self.org_client.create_organization(
            FeatureSet=featureset
        )

    def create_organization_unit(self, parentid, name):
        self.org_client.create_organizational_unit(
            ParentId=parentid,
            Name=name
        )

    def create_policy(self, content, description, name, orgtype):
        self.org_client.create_policy(
            Content=content,
            Description=description,
            Name=name,
            Type=orgtype
        )

    def delete_organization(self):
        self.org_client.delete_organization(
        )

    def delete_organization_unit(self, orgid):
        self.org_client.delete_organizational_unit(
            OrganizationalUnitId=orgid
        )

    def delete_policy(self, policyid):
        self.org_client.delete_policy(
            PolicyId=policyid
        )

    def describe_account(self, accountid):
        response = self.org_client.describe_account(
            AccountId=accountid
        )

        return response['Account']

    def describe_account_create_status(self, requestid):
        response = self.org_client.describe_create_account_status(
            CreateAccountRequestId=requestid
        )

        return response['CreateAccountStatus']

    def describe_organization(self):
        response = self.org_client.describe_organization(
        )

        return response['Organization']

    def describe_organization_unit(self, orgunitid):
        response = self.org_client.describe_organizational_unit(
            OrganizationalUnitId=orgunitid
        )

        return response['OrganizationalUnit']

    def describe_policy(self, policyid):
        response = self.org_client.describe_policy(
            PolicyId=policyid
        )

        return response['Policy']

    def detach_policy(self, policyid, targetid):
        self.org_client.detach_policy(
            PolicyId=policyid,
            TargetId=targetid
        )

    def disable_policy_type(self, rootid, policytype):
        self.org_client.disable_policy_type(
            RootId=rootid,
            PolicyType=policytype
        )

    def enable_policy_type(self, rootid, policytype):
        self.org_client.enable_policy_type(
            RootId=rootid,
            PolicyType=policytype
        )

    def invite_account_to_organization(self, targetid, targettype, notes):
        self.org_client.invite_account_to_organization(
            Target={
                'Id': targetid,
                'Type': targettype
            },
            Notes=notes
        )

    def list_accounts(self, parentid=None):
        accounts = []
        if parentid:
            response = self.org_client.list_accounts_for_parent(
                ParentId=parentid
            )
        else:
            response = self.org_client.list_accounts(
            )
        accounts.extend(response['Accounts'])
        while 'NextToken' in response:
            if parentid:
                response = self.org_client.list_accounts_for_parent(
                    ParentId=parentid,
                    NextToken=response['NextToken']
                )
            else:
                response = self.org_client.list_accounts(
                    NextToken=response['NextToken']
                )
            accounts.extend(response['Accounts'])

        return accounts

    def list_children(self, parentid, childtype):
        accounts = []
        response = self.org_client.list_children(
            ParentId=parentid,
            ChildType=childtype
        )
        accounts.extend(response['Children'])
        while 'NextToken' in response:
            response = self.org_client.list_children(
                ParentId=parentid,
                ChildType=childtype,
                NextToken=response['NextToken']
            )
            accounts.extend(response['Children'])

        return accounts

    def list_create_account_status(self, states, nexttoken=None, maxresults=None):
        accounts = []
        response = self.org_client.list_create_account_status(
            States=states,
            NextToken=nexttoken,
            MaxResults=maxresults
        )
        accounts.extend(response['CreateAccountStatuses'])
        while 'NextToken' in response:
            response = self.org_client.list_create_account_status(
                States=states,
                NextToken=response['NextToken'],
                MaxResults=maxresults
            )
            accounts.extend(response['CreateAccountStatuses'])

        return accounts

    def list_handshakes(self, account=True, handshakefilter=None, nexttoken=None, maxresults=None):
        handshakes = []
        if account:
            response = self.org_client.list_handshakes_for_account(
                Filter=handshakefilter,
                NextToken=nexttoken,
                MaxResults=maxresults
            )
        else:
            response = self.org_client.list_handshakes_for_organization(
                Filter=handshakefilter,
                NextToken=nexttoken,
                MaxResults=maxresults
            )
        handshakes.extend(response['Handshakes'])
        while 'NextToken' in response:
            if account:
                response = self.org_client.list_handshakes_for_account(
                    Filter=handshakefilter,
                    NextToken=response['NextToken'],
                    MaxResults=maxresults
                )
            else:
                response = self.org_client.list_handshakes_for_organization(
                    Filter=handshakefilter,
                    NextToken=response['NextToken'],
                    MaxResults=maxresults
                )
            handshakes.extend(response['Handshakes'])

        return handshakes

    def list_organizational_units_for_parent(self, parentid, nexttoken=None, maxresults=None):
        org_units = []
        response = self.org_client.list_organizational_units_for_parent(
            ParentId=parentid,
            NextToken=nexttoken,
            MaxResults=maxresults
        )
        org_units.extend(response['OrganizationalUnits'])
        while 'NextToken' in response:
            response = self.org_client.list_organizational_units_for_parent(
                ParentId=parentid,
                NextToken=response['NextToken'],
                MaxResults=maxresults
            )
            org_units.extend(response['OrganizationalUnits'])

        return org_units

    def list_parents(self, childid, nexttoken=None, maxresults=None):
        parents = []
        response = self.org_client.list_parents(
            ChildId=childid,
            NextToken=nexttoken,
            MaxResults=maxresults
        )
        parents.extend(response['Parents'])
        while 'NextToken' in response:
            response = self.org_client.list_parents(
                ChildId=childid,
                NextToken=response['NextToken'],
                MaxResults=maxresults
            )
            parents.extend(response['Parents'])

        return parents

    def list_policies(self, targetid, policyfilter=None, nexttoken=None, maxresults=None):
        if policyfilter is None:
            policyfilter = []
        policies = []
        if targetid:
            response = self.org_client.list_policies_for_target(
                TargetId=targetid,
                Filter=policyfilter,
                NextToken=nexttoken,
                MaxResults=maxresults
            )
        else:
            response = self.org_client.list_parents(
                Filter=policyfilter,
                NextToken=nexttoken,
                MaxResults=maxresults
            )
        policies.extend(response['Policies'])
        while 'NextToken' in response:
            if targetid:
                response = self.org_client.list_policies_for_target(
                    TargetId=targetid,
                    Filter=policyfilter,
                    NextToken=response['NextToken'],
                    MaxResults=maxresults
                )
            else:
                response = self.org_client.list_parents(
                    Filter=policyfilter,
                    NextToken=response['NextToken'],
                    MaxResults=maxresults
                )
            policies.extend(response['Policies'])

        return policies

    def list_roots(self):
        roots = []
        response = self.org_client.list_roots()
        roots.extend(response['Roots'])

        while 'NextToken' in response:
            response = self.org_client.list_roots(
                NextToken=response['NextToken']
            )
            roots.extend(response['Roots'])

        return roots

    def list_targets_for_policy(self, policyid, nexttoken=None, maxresults=None):
        targets = []
        response = self.org_client.list_targets_for_policy(
            PolicyId=policyid,
            NextToken=nexttoken,
            MaxResults=maxresults
        )
        targets.extend(response['Targets'])
        while 'NextToken' in response:
            response = self.org_client.list_targets_for_policy(
                PolicyId=policyid,
                NextToken=response['NextToken'],
                MaxResults=maxresults
            )
            targets.extend(response['Targets'])

        return targets

    def move_account(self, accountid, sourceid, destinationid):
        self.org_client.move_account(
            AccountId=accountid,
            SourceParentId=sourceid,
            DestinationParentId=destinationid
        )

    def remove_account_from_organization(self, accountid):
        self.org_client.remove_account_from_organization(
            AccountId=accountid
        )

    def update_organizational_unit(self, orgid, name):
        self.org_client.update_organizational_unit(
            OrganizationalUnitId=orgid,
            Name=name
        )

    def update_policy(self, policyid, name, description, content):
        self.org_client.update_policy(
            PolicyId=policyid,
            Name=name,
            Description=description,
            Content=content
        )
