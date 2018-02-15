import unittest

from mock import MagicMock

from PyStacks.PyStacks.organizationstasks import organizationstasks


class TestOrganizationsTasksSetup(unittest.TestCase):
    def setUp(self):
        self.mocksession = MagicMock()
        self.mockorgClient = MagicMock()

        self.mocksession.client.return_value = self.mockorgClient

        self.organizationstasks = organizationstasks()


class TestOrganizationsTasks(TestOrganizationsTasksSetup):
    def test_config_org_chart(self):
        config = {
            'test-account-core': {
                'test-account-iam': None,
                'test-account-build': None,
                'test-account-run': {
                    'test-account-nonprod': None,
                    'test-account-prod': None
                }
            }
        }
        assertorg = {
            "Children": [{
                "Children": [{
                    "Children": [],
                    "Name": "test-account-prod"
                }, {
                    "Children": [],
                    "Name": "test-account-nonprod"
                }],
                "Name": "test-account-run"
            }, {
                "Children": [],
                "Name": "test-account-iam"
            }, {
                "Children": [],
                "Name": "test-account-build"
            }],
            "Name": "test-account-core"
        }

        testorg = self.organizationstasks.config_organization_tree(config=config)
        self.assertEquals(testorg, assertorg)

    # def test_config_org_chart(self):
    #     aws_accounts = [
    #         {
    #             "Arn": "arn:aws:organizations::505500078186:account/o-jmksptn7tg/073913705544",
    #             "Id": "073913705544",
    #             "JoinedMethod": "CREATED",
    #             "JoinedTimestamp": "2017-05-01 05:21:16.356000+00:00",
    #             "Name": "aws-kablamo-prod",
    #             "Status": "ACTIVE"
    #         },
    #         {
    #             "Arn": "arn:aws:organizations::505500078186:account/o-jmksptn7tg/167464700695",
    #             "Id": "167464700695",
    #             "JoinedMethod": "CREATED",
    #             "JoinedTimestamp": "2017-05-01 05:21:37.694000+00:00",
    #             "Name": "aws-kablamo-demo",
    #             "Status": "ACTIVE"
    #         },
    #         {
    #             "Arn": "arn:aws:organizations::505500078186:account/o-jmksptn7tg/393141785041",
    #             "Id": "393141785041",
    #             "JoinedMethod": "CREATED",
    #             "JoinedTimestamp": "2017-05-01 04:18:22.009000+00:00",
    #             "Name": "aws-kablamo-build",
    #             "Status": "ACTIVE"
    #         },
    #         {
    #             "Arn": "arn:aws:organizations::505500078186:account/o-jmksptn7tg/505500078186",
    #             "Id": "505500078186",
    #             "JoinedMethod": "INVITED",
    #             "JoinedTimestamp": "2017-05-01 02:26:31.639000+00:00",
    #             "Name": "Allan Waddell",
    #             "Status": "ACTIVE"
    #         },
    #         {
    #             "Arn": "arn:aws:organizations::505500078186:account/o-jmksptn7tg/623551153426",
    #             "Id": "623551153426",
    #             "JoinedMethod": "CREATED",
    #             "JoinedTimestamp": "2017-05-01 04:02:14.833000+00:00",
    #             "Name": "aws-kablamo-iam",
    #             "Status": "ACTIVE"
    #         },
    #         {
    #             "Arn": "arn:aws:organizations::505500078186:account/o-jmksptn7tg/718583902179",
    #             "Id": "718583902179",
    #             "JoinedMethod": "CREATED",
    #             "JoinedTimestamp": "2017-05-01 04:20:33.896000+00:00",
    #             "Name": "aws-kablamo-dev",
    #             "Status": "ACTIVE"
    #         }
    #     ]
    #     config_orgs = {
    #         "aws-kablamo-build": {
    #             "Email": "aws-kablamo-build@kablamo.com.au",
    #             "IamUserAccess": "IamUserAccess",
    #             "Name": "aws-kablamo-build",
    #             "Rolename": "OrgAdminRole"
    #         },
    #         "aws-kablamo-demo": {
    #             "Email": "aws-kablamo-demo@kablamo.com.au",
    #             "IamUserAccess": "IamUserAccess",
    #             "Name": "aws-kablamo-demo",
    #             "Rolename": "OrgAdminRole"
    #         },
    #         "aws-kablamo-dev": {
    #             "Email": "aws-kablamo-dev@kablamo.com.au",
    #             "IamUserAccess": "IamUserAccess",
    #             "Name": "aws-kablamo-dev",
    #             "Rolename": "OrgAdminRole"
    #         },
    #         "aws-kablamo-iam": {
    #             "Email": "aws-kablamo-iam@kablamo.com.au",
    #             "IamUserAccess": "IamUserAccess",
    #             "Name": "aws-kablamo-iam",
    #             "Rolename": "OrgAdminRole"
    #         },
    #         "aws-kablamo-prod": {
    #             "Email": "aws-kablamo-prod@kablamo.com.au",
    #             "IamUserAccess": "IamUserAccess",
    #             "Name": "aws-kablamo-prod",
    #             "Rolename": "OrgAdminRole"
    #         },
    #         "aws-s2-iam": {
    #             "Email": "aws-s2-iam@kablamo.com.au",
    #             "IamUserAccess": "IamUserAccess",
    #             "Name": "aws-s2-iam",
    #             "Rolename": "OrgAdminRole"
    #         }
    #     }

    #     testorg = self.organizationstasks.config_organization_tree(config=config)
    #     self.assertEquals(testorg, assertorg)
