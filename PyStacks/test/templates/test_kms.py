import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_KMS(self):
        resources = {
            'kms': {
                'testkey': {
                    'description': 'testkeydescription',
                    'enabled': True,
                    'rotation': True,
                    'policy': '{ "somejsonobj": "something" }',
                    'aliasname': 'testkeyalias'
                }
            }
        }
        expected = {
            'testkey': {
                'Type': 'AWS::KMS::Key',
                'Properties': {
                    'Description': 'testkeydescription',
                    'Enabled': 'true',
                    'EnableKeyRotation': 'true',
                    'KeyPolicy': {
                        'somejsonobj': 'something'
                    }
                }
            },
            'testkeyAlias': {
                'Type': 'AWS::KMS::Alias',
                'Properties': {
                    'AliasName': 'alias/testkeyalias',
                    'TargetKeyId': {
                        'Ref': 'testkey'
                    }
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
