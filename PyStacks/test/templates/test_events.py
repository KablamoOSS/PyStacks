import unittest

from PyStacks.PyStacks.template import templateCF

EVENT_NAME = 'TestEventName'


class TestTemplate(unittest.TestCase):

    def test_templateCF_TestEvent(self):
        target = {
            'id': 'fooId',
            'arn': 'fooRef',
        }
        resources = {
            'events': {
                'testevent': {
                    'name': EVENT_NAME,
                    'description': 'test description',
                    'schedule': 'rate(10 minutes)',
                    'targets': [target],
                }
            }
        }
        testevent = resources['events']['testevent']
        expected = {
            'testevent': {
                'Type': 'AWS::Events::Rule',
                'Properties': {
                    'ScheduleExpression': testevent['schedule'],
                    'Targets': [
                        {
                            'Id': target['id'],
                            'Arn': {'Fn::GetAtt': [target['arn'], "Arn"]},
                        }
                    ],
                    'Description': testevent['description'],
                    'Name': testevent['name'],
                },
            }
        }
        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
