import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_ACM(self):
        resources = {
            "certificatemanager": {
                "shopkablamocomau": {
                    "domainname": "shop.kablamo.com.au",
                    "domainvalidationoptions": {
                        "shop.kablamo.com.au": "kablamo.com.au",
                        "www.shop.kablamo.com.au": "kablamo.com.au"
                    },
                    "subjectalternativenames": [
                        "www.shop.kablamo.com.au"
                    ],
                    "tags": {
                        "Name": "Shop Certificate"
                    }
                }
            }
        }
        expected = {
            "shopkablamocomau": {
                "Properties": {
                    "DomainName": "shop.kablamo.com.au",
                    "DomainValidationOptions": [
                        {
                            "DomainName": "www.shop.kablamo.com.au",
                            "ValidationDomain": "kablamo.com.au"
                        },
                        {
                            "DomainName": "shop.kablamo.com.au",
                            "ValidationDomain": "kablamo.com.au"
                        }
                    ],
                    "SubjectAlternativeNames": [
                        "www.shop.kablamo.com.au"
                    ],
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": "Shop Certificate"
                        }
                    ]
                },
                "Type": "AWS::CertificateManager::Certificate"
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
