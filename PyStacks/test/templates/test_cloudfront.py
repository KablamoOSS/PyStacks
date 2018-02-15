import unittest

from PyStacks.PyStacks.template import templateCF


class TestTemplate(unittest.TestCase):

    def test_templateCF_CloudFront(self):
        resources = {
            'cloudfront': {
                'testmultiplecloudfronts': {
                    'aliases': [
                        'alias1',
                        'alias2'
                    ],
                    'cachebehaviors': [
                        {
                            'allowedmethods': [
                                'GET',
                                'POST'
                            ],
                            'cachedmethods': [
                                'GET',
                                'POST'
                            ],
                            'compress': True,
                            'defaultttl': '300',
                            'cookies': 'all',
                            'headers': [
                                'header1',
                                'header2'
                            ],
                            'querystring': 'querystringtest',
                            'querystringkeys': [
                                'querystringkey1',
                                'querystringkey2'
                            ],
                            'maxttl': '600',
                            'minttl': '60',
                            'pathpattern': '^$',
                            'targetoriginid': 'targetoriginidtest',
                            'viewerprotocolpolicy': 'viewerprotocolpolicytest'
                        },
                        {
                            'allowedmethods': [
                                'DELETE'
                            ],
                            'cachedmethods': [
                                'DELETE'
                            ],
                            'compress': True,
                            'defaultttl': '300',
                            'cookies': 'all',
                            'headers': [
                                'header1',
                                'header2'
                            ],
                            'querystring': 'querystringtest',
                            'querystringkeys': [
                                'querystringkey1',
                                'querystringkey2'
                            ],
                            'maxttl': '600',
                            'minttl': '60',
                            'pathpattern': '^$',
                            'targetoriginid': 'targetoriginidtest',
                            'viewerprotocolpolicy': 'viewerprotocolpolicytest'
                        }
                    ],
                    'comment': 'somecomment',
                    'customerrorresponses': [
                        {
                            'errorcachingminttl': 60,
                            'errorcode': 500,
                            'responsecode': 403,
                            'responsepagepath': '/error.html'
                        },
                        {
                            'errorcachingminttl': 60,
                            'errorcode': 503,
                            'responsecode': 403,
                            'responsepagepath': '/error.html'
                        }
                    ],
                    'defaultbehaviors': {
                        'allowedmethods': [
                            'GET',
                            'POST'
                        ],
                        'cachedmethods': [
                            'GET',
                            'POST'
                        ],
                        'compress': True,
                        'defaultttl': '300',
                        'cookies': 'all',
                        'headers': [
                            'header1',
                            'header2'
                        ],
                        'querystring': 'querystringtest',
                        'querystringkeys': [
                            'querystringkey1',
                            'querystringkey2'
                        ],
                        'maxttl': '600',
                        'minttl': '60',
                        'targetoriginid': 'targetoriginidtest',
                        'viewerprotocolpolicy': 'viewerprotocolpolicytest'
                    },
                    'defaultrootobject': '/index.html',
                    'enabled': True,
                    'httpversion': '1.2',
                    'logging': {
                        'includecookies': True,
                        'bucket': 'testbucket',
                        'prefix': 'dev-'
                    },
                    'priceclass': 'testpriceclass',
                    'viewercertificate': 'testviewercertarn',
                    'webaclid': 'webaclidtest',
                    'origins': [
                        {
                            'domain': 'example.com',
                            'id': 'originidtest',
                            'originpath': '/',
                            'http': '80',
                            'https': '443',
                            'protocolpolicy': 'testprotocolpolicy',
                            'origincustomheaders': {
                                'Headername1': 'headervalue1',
                                'Headername2': 'headervalue2'
                            }
                        },
                        {
                            'domain': 'example2.com',
                            'id': 'originidtest2',
                            'http': '8080',
                            'https': '8443',
                            'protocolpolicy': 'testprotocolpolicy2',
                            'origincustomheaders': {
                                'Headername1': 'headervalue1',
                                'Headername2': 'headervalue2'
                            }
                        }
                    ]
                },
                'testcloudfront': {
                    'aliases': [
                        'alias1',
                        'alias2'
                    ],
                    'cachebehaviors': [
                        {
                            'allowedmethods': [
                                'GET',
                                'POST'
                            ],
                            'cachedmethods': [
                                'GET',
                                'POST'
                            ],
                            'compress': True,
                            'defaultttl': '300',
                            'cookies': 'all',
                            'headers': [
                                'header1',
                                'header2'
                            ],
                            'querystring': 'querystringtest',
                            'querystringkeys': [
                                'querystringkey1',
                                'querystringkey2'
                            ],
                            'maxttl': '600',
                            'minttl': '60',
                            'pathpattern': '^$',
                            'targetoriginid': 'targetoriginidtest',
                            'viewerprotocolpolicy': 'viewerprotocolpolicytest'
                        },
                        {
                            'allowedmethods': [
                                'DELETE'
                            ],
                            'cachedmethods': [
                                'DELETE'
                            ],
                            'compress': True,
                            'defaultttl': '300',
                            'cookies': 'all',
                            'headers': [
                                'header1',
                                'header2'
                            ],
                            'querystring': 'querystringtest',
                            'querystringkeys': [
                                'querystringkey1',
                                'querystringkey2'
                            ],
                            'maxttl': '600',
                            'minttl': '60',
                            'pathpattern': '^$',
                            'targetoriginid': 'targetoriginidtest',
                            'viewerprotocolpolicy': 'viewerprotocolpolicytest'
                        }
                    ],
                    'comment': 'somecomment',
                    'customerrorresponses': [
                        {
                            'errorcachingminttl': 60,
                            'errorcode': 500,
                            'responsecode': 403,
                            'responsepagepath': '/error.html'
                        },
                        {
                            'errorcachingminttl': 60,
                            'errorcode': 503,
                            'responsecode': 403,
                            'responsepagepath': '/error.html'
                        }
                    ],
                    'defaultbehaviors': {
                        'allowedmethods': [
                            'GET',
                            'POST'
                        ],
                        'cachedmethods': [
                            'GET',
                            'POST'
                        ],
                        'compress': True,
                        'defaultttl': '300',
                        'cookies': 'all',
                        'headers': [
                            'header1',
                            'header2'
                        ],
                        'querystring': 'querystringtest',
                        'querystringkeys': [
                            'querystringkey1',
                            'querystringkey2'
                        ],
                        'maxttl': '600',
                        'minttl': '60',
                        'targetoriginid': 'targetoriginidtest',
                        'viewerprotocolpolicy': 'viewerprotocolpolicytest'
                    },
                    'defaultrootobject': '/index.html',
                    'enabled': True,
                    'httpversion': '1.2',
                    'logging': {
                        'includecookies': True,
                        'bucket': 'testbucket',
                        'prefix': 'dev-'
                    },
                    'priceclass': 'testpriceclass',
                    'viewercertificate': 'testviewercertarn',
                    'webaclid': 'webaclidtest',
                    'origins': [
                        {
                            'domain': 'example.com',
                            'id': 'originidtest',
                            'originpath': '/',
                            'http': '80',
                            'https': '443',
                            'protocolpolicy': 'testprotocolpolicy',
                            'origincustomheaders': {
                                'Headername1': 'headervalue1',
                                'Headername2': 'headervalue2'
                            }
                        },
                        {
                            'domain': 'example2.com',
                            'id': 'originidtest2',
                            'http': '8080',
                            'https': '8443',
                            'protocolpolicy': 'testprotocolpolicy2',
                            'origincustomheaders': {
                                'Headername1': 'headervalue1',
                                'Headername2': 'headervalue2'
                            }
                        }
                    ]
                }
            }
        }
        expected = {
            'testmultiplecloudfronts': {
                'Type': 'AWS::CloudFront::Distribution',
                'Properties': {
                    'DistributionConfig': {
                        'Aliases': [
                            'alias1',
                            'alias2'
                        ],
                        'CacheBehaviors': [
                            {
                                'AllowedMethods': [
                                    'GET',
                                    'POST'
                                ],
                                'CachedMethods': [
                                    'GET',
                                    'POST'
                                ],
                                'Compress': 'true',
                                'DefaultTTL': '300',
                                'ForwardedValues': {
                                    'Cookies': {
                                        'Forward': 'all'
                                    },
                                    'Headers': [
                                        'header1',
                                        'header2'
                                    ],
                                    'QueryString': 'querystringtest',
                                    'QueryStringCacheKeys': [
                                        'querystringkey1',
                                        'querystringkey2'
                                    ]
                                },
                                'MaxTTL': '600',
                                'MinTTL': '60',
                                'PathPattern': '^$',
                                'TargetOriginId': 'targetoriginidtest',
                                'ViewerProtocolPolicy': 'viewerprotocolpolicytest'
                            },
                            {
                                'AllowedMethods': [
                                    'DELETE'
                                ],
                                'CachedMethods': [
                                    'DELETE'
                                ],
                                'Compress': 'true',
                                'DefaultTTL': '300',
                                'ForwardedValues': {
                                    'Cookies': {
                                        'Forward': 'all'
                                    },
                                    'Headers': [
                                        'header1',
                                        'header2'
                                    ],
                                    'QueryString': 'querystringtest',
                                    'QueryStringCacheKeys': [
                                        'querystringkey1',
                                        'querystringkey2'
                                    ]
                                },
                                'MaxTTL': '600',
                                'MinTTL': '60',
                                'PathPattern': '^$',
                                'TargetOriginId': 'targetoriginidtest',
                                'ViewerProtocolPolicy': 'viewerprotocolpolicytest'
                            }
                        ],
                        'Comment': 'somecomment',
                        'CustomErrorResponses': [
                            {
                                'ErrorCachingMinTTL': '60',
                                'ErrorCode': '500',
                                'ResponseCode': '403',
                                'ResponsePagePath': '/error.html'
                            },
                            {
                                'ErrorCachingMinTTL': '60',
                                'ErrorCode': '503',
                                'ResponseCode': '403',
                                'ResponsePagePath': '/error.html'
                            }
                        ],
                        'DefaultCacheBehavior': {
                            'AllowedMethods': [
                                'GET',
                                'POST'
                            ],
                            'CachedMethods': [
                                'GET',
                                'POST'
                            ],
                            'Compress': 'true',
                            'DefaultTTL': '300',
                            'ForwardedValues': {
                                'Cookies': {
                                    'Forward': 'all'
                                },
                                'Headers': [
                                    'header1',
                                    'header2'
                                ],
                                'QueryString': 'querystringtest',
                                'QueryStringCacheKeys': [
                                    'querystringkey1',
                                    'querystringkey2'
                                ]
                            },
                            'MaxTTL': '600',
                            'MinTTL': '60',
                            'TargetOriginId': 'targetoriginidtest',
                            'ViewerProtocolPolicy': 'viewerprotocolpolicytest'
                        },
                        'DefaultRootObject': '/index.html',
                        'Enabled': 'true',
                        'HttpVersion': '1.2',
                        'Logging': {
                            'IncludeCookies': 'true',
                            'Bucket': 'testbucket',
                            'Prefix': 'dev-'
                        },
                        'PriceClass': 'testpriceclass',
                        'ViewerCertificate': {
                            'AcmCertificateArn': 'testviewercertarn',
                            'SslSupportMethod': 'sni-only'
                        },
                        'WebACLId': 'webaclidtest',
                        'Origins': [
                            {
                                'DomainName': 'example.com',
                                'Id': 'originidtest',
                                'OriginPath': '/',
                                'OriginCustomHeaders': [
                                    {
                                        'HeaderName': 'Headername1',
                                        'HeaderValue': 'headervalue1'
                                    },
                                    {
                                        'HeaderName': 'Headername2',
                                        'HeaderValue': 'headervalue2'
                                    }
                                ],
                                'CustomOriginConfig': {
                                    'HTTPPort': '80',
                                    'HTTPSPort': '443',
                                    'OriginProtocolPolicy': 'testprotocolpolicy'
                                }
                            },
                            {
                                'DomainName': 'example2.com',
                                'Id': 'originidtest2',
                                'OriginCustomHeaders': [
                                    {
                                        'HeaderName': 'Headername1',
                                        'HeaderValue': 'headervalue1'
                                    },
                                    {
                                        'HeaderName': 'Headername2',
                                        'HeaderValue': 'headervalue2'
                                    }
                                ],
                                'CustomOriginConfig': {
                                    'HTTPPort': '8080',
                                    'HTTPSPort': '8443',
                                    'OriginProtocolPolicy': 'testprotocolpolicy2'
                                }
                            }
                        ]
                    }
                }
            },
            'testcloudfront': {
                'Type': 'AWS::CloudFront::Distribution',
                'Properties': {
                    'DistributionConfig': {
                        'Aliases': [
                            'alias1',
                            'alias2'
                        ],
                        'CacheBehaviors': [
                            {
                                'AllowedMethods': [
                                    'GET',
                                    'POST'
                                ],
                                'CachedMethods': [
                                    'GET',
                                    'POST'
                                ],
                                'Compress': 'true',
                                'DefaultTTL': '300',
                                'ForwardedValues': {
                                    'Cookies': {
                                        'Forward': 'all'
                                    },
                                    'Headers': [
                                        'header1',
                                        'header2'
                                    ],
                                    'QueryString': 'querystringtest',
                                    'QueryStringCacheKeys': [
                                        'querystringkey1',
                                        'querystringkey2'
                                    ]
                                },
                                'MaxTTL': '600',
                                'MinTTL': '60',
                                'PathPattern': '^$',
                                'TargetOriginId': 'targetoriginidtest',
                                'ViewerProtocolPolicy': 'viewerprotocolpolicytest'
                            },
                            {
                                'AllowedMethods': [
                                    'DELETE'
                                ],
                                'CachedMethods': [
                                    'DELETE'
                                ],
                                'Compress': 'true',
                                'DefaultTTL': '300',
                                'ForwardedValues': {
                                    'Cookies': {
                                        'Forward': 'all'
                                    },
                                    'Headers': [
                                        'header1',
                                        'header2'
                                    ],
                                    'QueryString': 'querystringtest',
                                    'QueryStringCacheKeys': [
                                        'querystringkey1',
                                        'querystringkey2'
                                    ]
                                },
                                'MaxTTL': '600',
                                'MinTTL': '60',
                                'PathPattern': '^$',
                                'TargetOriginId': 'targetoriginidtest',
                                'ViewerProtocolPolicy': 'viewerprotocolpolicytest'
                            }
                        ],
                        'Comment': 'somecomment',
                        'CustomErrorResponses': [
                            {
                                'ErrorCachingMinTTL': '60',
                                'ErrorCode': '500',
                                'ResponseCode': '403',
                                'ResponsePagePath': '/error.html'
                            },
                            {
                                'ErrorCachingMinTTL': '60',
                                'ErrorCode': '503',
                                'ResponseCode': '403',
                                'ResponsePagePath': '/error.html'
                            }
                        ],
                        'DefaultCacheBehavior': {
                            'AllowedMethods': [
                                'GET',
                                'POST'
                            ],
                            'CachedMethods': [
                                'GET',
                                'POST'
                            ],
                            'Compress': 'true',
                            'DefaultTTL': '300',
                            'ForwardedValues': {
                                'Cookies': {
                                    'Forward': 'all'
                                },
                                'Headers': [
                                    'header1',
                                    'header2'
                                ],
                                'QueryString': 'querystringtest',
                                'QueryStringCacheKeys': [
                                    'querystringkey1',
                                    'querystringkey2'
                                ]
                            },
                            'MaxTTL': '600',
                            'MinTTL': '60',
                            'TargetOriginId': 'targetoriginidtest',
                            'ViewerProtocolPolicy': 'viewerprotocolpolicytest'
                        },
                        'DefaultRootObject': '/index.html',
                        'Enabled': 'true',
                        'HttpVersion': '1.2',
                        'Logging': {
                            'IncludeCookies': 'true',
                            'Bucket': 'testbucket',
                            'Prefix': 'dev-'
                        },
                        'PriceClass': 'testpriceclass',
                        'ViewerCertificate': {
                            'AcmCertificateArn': 'testviewercertarn',
                            'SslSupportMethod': 'sni-only'
                        },
                        'WebACLId': 'webaclidtest',
                        'Origins': [
                            {
                                'DomainName': 'example.com',
                                'Id': 'originidtest',
                                'OriginPath': '/',
                                'OriginCustomHeaders': [
                                    {
                                        'HeaderName': 'Headername1',
                                        'HeaderValue': 'headervalue1'
                                    },
                                    {
                                        'HeaderName': 'Headername2',
                                        'HeaderValue': 'headervalue2'
                                    }
                                ],
                                'CustomOriginConfig': {
                                    'HTTPPort': '80',
                                    'HTTPSPort': '443',
                                    'OriginProtocolPolicy': 'testprotocolpolicy'
                                }
                            },
                            {
                                'DomainName': 'example2.com',
                                'Id': 'originidtest2',
                                'OriginCustomHeaders': [
                                    {
                                        'HeaderName': 'Headername1',
                                        'HeaderValue': 'headervalue1'
                                    },
                                    {
                                        'HeaderName': 'Headername2',
                                        'HeaderValue': 'headervalue2'
                                    }
                                ],
                                'CustomOriginConfig': {
                                    'HTTPPort': '8080',
                                    'HTTPSPort': '8443',
                                    'OriginProtocolPolicy': 'testprotocolpolicy2'
                                }
                            }
                        ]
                    }
                }
            }
        }

        actual = templateCF(resources, 'resources')
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
