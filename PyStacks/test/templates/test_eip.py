import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_EIP(self):
        resources = {
            'eip': {
                'test1',
                'test2.3-4'
            }
        }
        expected = {
            'test1EIP': {
                'Type': 'AWS::EC2::EIP',
                'Properties': {
                    'InstanceId': {'Ref': 'test1'},
                    'Domain': 'vpc'
                }
            },
            'test234EIP': {
                'Type': 'AWS::EC2::EIP',
                'Properties': {
                    'InstanceId': {'Ref': 'test234'},
                    'Domain': 'vpc'
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
