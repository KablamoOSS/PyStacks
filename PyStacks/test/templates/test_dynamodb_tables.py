import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_GenericDynamoDbTables(self):
        resources = {
            'dynamodb_tables': {
                'testTable': {
                    'name': 'testTable',
                    'attributes': [
                        {
                            'name': 'keyAttribute',
                            'type': 'S'
                        }
                    ],
                    'key_schema': [
                        {
                            'name': 'keyAttribute',
                            'type': 'HASH'
                        },
                    ],
                    'throughput': {
                        'read_units': 10,
                        'write_units': 1
                    },
                    'stream': {
                        'type': "NEW_IMAGE"
                    },
                },
            },
        }
        expected = {
            "testTable": {
                "Type": "AWS::DynamoDB::Table",
                "Properties": {
                    "AttributeDefinitions": [
                        {
                            "AttributeName": "keyAttribute",
                            "AttributeType": "S"
                        },
                    ],
                    "KeySchema": [
                        {
                            "AttributeName": "keyAttribute",
                            "KeyType": "HASH"
                        },
                    ],
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": "10",
                        "WriteCapacityUnits": "1"
                    },
                    "StreamSpecification": {
                        "StreamViewType": "NEW_IMAGE"
                    },
                    "TableName": "testTable"
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
