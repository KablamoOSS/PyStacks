import unittest
import json
import pprint

from PyStacks.PyStacks.ecs import template_service_cf


class testHelper():
    @staticmethod
    def contains(container, contained):
        '''ensure that `contained` is present in `container`. This ignores siblings, but maintain structure

            EXAMPLES:

            contains(
                {'a': 3, 'b': 4},
                {'a': 3}
            ) # True

            contains(
                {'a': [3, 4, 5]},
                {'a': 3},
            ) # False

            contains(
                {'a': [3, 4, 5]},
                {'a': [3]},
            ) # True

            contains(
                {'a': 4, 'b': {'a':3}},
                {'a': 3}
            ) # False

            contains(
                {'a': 4, 'b': {'a':3, 'c': 5}},
                {'a': 3, 'c': 5}
            ) # False

            # if an `contained` has a list, then every item from that list must be present
            # in the corresponding `container` list
            contains(
                {'a': [{'b':1}, {'b':2}, {'b':3}], 'c':4},
                {'a': [{'b':1},{'b':2}], 'c':4},
            ) # True

        '''
        if container == contained:
            return True

        if isinstance(container, list):
            if not isinstance(contained, list):
                return False
            true_count = 0
            for contained_item in contained:
                for item in container:
                    if testHelper.contains(item, contained_item):
                        true_count += 1
                        break
            if true_count == len(contained):
                return True

        if isinstance(contained, dict) and isinstance(container, dict):
            contained_keys = set(contained.keys())
            container_keys = set(container.keys())
            if len(contained_keys - container_keys) == 0:
                # then all the contained keys are in this container ~ recursive check
                if all(
                    testHelper.contains(container[key], contained[key])
                    for key in contained_keys
                ):
                    return True

        return False

    @staticmethod
    def formatDicts(expected, actual, msg="Expected this to exist:"):
        toReturn = \
        """

{msgExpected}
#######
{expectedDict}
#######

Actual:
#######
{actualDict}
#######
        """.format(  # noqa: E122
            msgExpected=msg,
            expectedDict=pprint.pformat(expected),
            actualDict=pprint.pformat(actual)
        )
        return toReturn

    @staticmethod
    def assertEcsRenderInclude(test, expectInclude, withInput={'service': {}}, taskArn="dontcare"):
        actual = json.loads(template_service_cf(taskArn, **withInput))
        test.assertTrue(
            testHelper.contains(actual, expectInclude),
            testHelper.formatDicts(expectInclude, actual))

    @staticmethod
    def assertEcsRenderExclude(test, expectExclude, withInput={'service': {}}):
        actual = json.loads(template_service_cf("dontcare", **withInput))
        test.assertFalse(
            testHelper.contains(actual, expectExclude),
            testHelper.formatDicts(expectExclude, actual, "Expected this to be missing:"))


class TestTemplate(unittest.TestCase):

    def test_should_render_serviceName_as_description(self):
        serviceName = 'myServiceName'
        yml = {
            'service': {
                'serviceName': serviceName
            }
        }
        expected = {
            'Description': serviceName
        }
        testHelper.assertEcsRenderInclude(self, withInput=yml, expectInclude=expected)

    def test_should_render_serviceName_in_output(self):
        serviceName = 'myServiceName'
        yml = {
            'service': {
                'serviceName': serviceName
            }
        }
        expected = {
            'Outputs': {
                'ServiceName': {
                    'Value': serviceName
                }
            }
        }
        testHelper.assertEcsRenderInclude(self, withInput=yml, expectInclude=expected)

    def test_should_render_cluster_in_service_resource_properties(self):
        cluster = 'myCluster'
        yml = {
            'service': {
                'cluster': cluster
            }
        }
        expected = {
            'Resources': {
                'service': {
                    'Properties': {
                        'Cluster': cluster
                    }
                }
            }
        }
        testHelper.assertEcsRenderInclude(self, withInput=yml, expectInclude=expected)

    def test_should_render_cluster_in_output(self):
        cluster = 'myCluster'
        yml = {
            'service': {
                'cluster': cluster
            }
        }
        expected = {
            'Outputs': {
                'ClusterName': {
                    'Value': cluster
                }
            }
        }
        testHelper.assertEcsRenderInclude(self, withInput=yml, expectInclude=expected)

    def test_should_render_minmaxHealth_in_deployment_configuration(self):
        minhealth = '20'
        maxhealth = '100'
        yml = {
            'service': {
                'minHealth': minhealth,
                'maxHealth': maxhealth
            }
        }
        expected = {
            'Resources': {
                'service': {
                    'Properties': {
                        'DeploymentConfiguration': {
                            'MinimumHealthyPercent': minhealth,
                            'MaximumPercent': maxhealth
                        }
                    }
                }
            }
        }
        testHelper.assertEcsRenderInclude(self, withInput=yml, expectInclude=expected)

    def test_should_render_desiredCount_in_service_resource_properties(self):
        desiredCount = '1'
        yml = {
            'service': {
                'desiredCount': desiredCount
            }
        }
        expected = {
            'Resources': {
                'service': {
                    'Properties': {
                        'DesiredCount': desiredCount
                    }
                }
            }
        }
        testHelper.assertEcsRenderInclude(self, withInput=yml, expectInclude=expected)

    def test_should_render_task_arn_as_task_definition(self):
        taskArn = 'myTaskArn'
        expected = {
            'Resources': {
                'service': {
                    'Properties': {
                        'TaskDefinition': taskArn
                    }
                }
            }
        }
        testHelper.assertEcsRenderInclude(self, taskArn=taskArn, expectInclude=expected)

    def test_should_render_constants(self):
        expected = {
            'AWSTemplateFormatVersion': '2010-09-09',
            'Resources': {
                'service': {
                    'Type': 'AWS::ECS::Service'
                }
            },
            'Outputs': {
                'ServiceArn': {
                    'Description': 'ServiceArn',
                    'Value': {'Ref': 'service'}
                }
            }

        }
        testHelper.assertEcsRenderInclude(self, expectInclude=expected)

    def test_should_NOT_render_loadbalancers_and_role_by_default(self):
        loadBalancers = {
            'Resources': {
                'service': {
                    'Properties': {
                        'LoadBalancers': [
                        ],
                        'Role': ''
                    }
                }
            }
        }
        testHelper.assertEcsRenderExclude(self, expectExclude=loadBalancers)

    def test_should_NOT_render_dependson_by_default(self):
        dependsOn = {
            'Resources': {
                'service': {
                    'DependsOn': [
                        'elb',
                        'targetgroup',
                        'listener'
                    ]
                }
            }
        }
        testHelper.assertEcsRenderExclude(self, expectExclude=dependsOn)

    def test_should_render_loadbalancers_and_role_with_elb(self):
        containername = 'myContainerName'
        containerport = 'myContainerPort'
        servicerole = 'myServiceRole'
        yml = {
            'service': {
                'containername': containername,
                'containerport': containerport,
                'servicerole': servicerole
            },
            'elb': {'dontcare': 'dontcare'}
        }
        loadBalancers = {
            'Resources': {
                'service': {
                    'Properties': {
                        'LoadBalancers': [
                            {
                                'ContainerName': containername,
                                'ContainerPort': containerport,
                                'TargetGroupArn': {
                                    'Ref': 'targetgroup'
                                }
                            }
                        ],
                        'Role': servicerole
                    }
                }
            }
        }
        testHelper.assertEcsRenderInclude(self, withInput=yml, expectInclude=loadBalancers)

    def test_should_render_dependson_with_elb(self):
        yml = {
            'service': {},
            'elb': {'dontcare': 'dontcare'}
        }
        dependsOn = {
            'Resources': {
                'service': {
                    'DependsOn': [
                        'elb',
                        'targetgroup',
                        'listener'
                    ]
                }
            }
        }
        testHelper.assertEcsRenderInclude(self, withInput=yml, expectInclude=dependsOn)

    def test_should_render_targetgroup_with_elb(self):
        healthcheckpath = '/health'
        servicename = 'myservicename'
        vpcid = 'myVpcID'
        yml = {
            'service': {
                'hcPath': healthcheckpath,
                'serviceName': servicename
            },
            'elb': {
                'vpcId': vpcid
            }
        }
        targetGroup = {
            'Resources': {
                'targetgroup': {
                    'Type': 'AWS::ElasticLoadBalancingV2::TargetGroup',
                    'Properties': {
                        'HealthCheckIntervalSeconds': 10,
                        'HealthCheckPath': healthcheckpath,
                        'HealthCheckTimeoutSeconds': 5,
                        'HealthyThresholdCount': 5,
                        'Name': servicename + "-tg",
                        'Port': 80,
                        'Protocol': 'HTTP',
                        'UnhealthyThresholdCount': 5,
                        'VpcId': vpcid
                    }
                }
            }
        }
        testHelper.assertEcsRenderInclude(self, withInput=yml, expectInclude=targetGroup)

    def test_should_render_targetgroup_default_matcher_with_elb(self):
        yml = {
            'service': {},
            'elb': {
                'dontcare': 'dontcare'
            }
        }
        targetGroup = {
            'Resources': {
                'targetgroup': {
                    'Type': 'AWS::ElasticLoadBalancingV2::TargetGroup',
                    'Properties': {
                        'Matcher': {
                            'HttpCode': '200'
                        }
                    }
                }
            }
        }
        testHelper.assertEcsRenderInclude(self, withInput=yml, expectInclude=targetGroup)

    def test_should_render_targetgroup_matcher_with_elb(self):
        httpCodeMatcher = '301'
        yml = {
            'service': {
                'hcHttpCodeMatcher': httpCodeMatcher
            },
            'elb': {
                'dontcare': 'dontcare'
            }
        }
        targetGroup = {
            'Resources': {
                'targetgroup': {
                    'Type': 'AWS::ElasticLoadBalancingV2::TargetGroup',
                    'Properties': {
                        'Matcher': {
                            'HttpCode': httpCodeMatcher
                        }
                    }
                }
            }
        }
        testHelper.assertEcsRenderInclude(self, withInput=yml, expectInclude=targetGroup)

    def test_should_render_listener_with_elb(self):
        port = '8787'
        protocol = 'https'
        yml = {
            'service': {},
            'elb': {
                'elbport': port,
                'elbproto': protocol
            }
        }
        listener = {
            'Resources': {
                'listener': {
                    'Type': 'AWS::ElasticLoadBalancingV2::Listener',
                    'Properties': {
                        'DefaultActions': [{
                            'TargetGroupArn': {'Ref': 'targetgroup'},
                            'Type': 'forward'
                        }],
                        'LoadBalancerArn': {'Ref': 'elb'},
                        'Port': port,
                        'Protocol': protocol
                    },
                    'DependsOn': [
                        'elb',
                        'targetgroup'
                    ]
                }
            }
        }
        testHelper.assertEcsRenderInclude(self, withInput=yml, expectInclude=listener)

    def test_should_NOT_render_listener_certificates_without_elb_sslid(self):
        yml = {
            'service': {},
            'elb': {
                'dontcare': 'dontcare'
            }
        }
        listener = {
            'Resources': {
                'listener': {
                    'Properties': {
                        'Certificates': [{
                            'CertificateArn': ''
                        }]
                    }
                }
            }
        }
        testHelper.assertEcsRenderExclude(self, withInput=yml, expectExclude=listener)

    def test_should_render_listener_certificates_with_elb_sslid(self):
        sslid = 'mySSLID'
        yml = {
            'service': {},
            'elb': {
                'sslid': sslid
            }
        }
        listener = {
            'Resources': {
                'listener': {
                    'Properties': {
                        'Certificates': [{
                            'CertificateArn': sslid
                        }]
                    }
                }
            }
        }
        testHelper.assertEcsRenderInclude(self, withInput=yml, expectInclude=listener)


if __name__ == '__main__':
    unittest.main()
