import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_Athena_NamedQuery(self):
        resources = {
            "athena_namedquery": {
                "samplequery": {
                    "description": "samplequery",
                    "querystring": "SELECT workflowname, AVG(activitytaskstarted) AS AverageWorkflow FROM swfmetadata WHERE year='17' AND GROUP BY workflowname ORDER BY AverageWorkflow DESC LIMIT 10",
                    "database": "sampledb",
                    "name": "SampleQuery"
                }
            }
        }
        expected = {
            "samplequery": {
                "Properties": {
                    "Database": "sampledb",
                    "Description": "samplequery",
                    "Name": "SampleQuery",
                    "QueryString": "SELECT workflowname, AVG(activitytaskstarted) AS AverageWorkflow FROM swfmetadata WHERE year='17' AND GROUP BY workflowname ORDER BY AverageWorkflow DESC LIMIT 10"
                },
                "Type": "AWS::Athena::NamedQuery"
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
