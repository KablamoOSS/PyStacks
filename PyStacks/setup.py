from setuptools import setup

setup(
    name='PyStacks',
    version='0.1',
    description='AWS automation tool.',
    url='https://github.com/KablamoOSS/PyStacks.git',
    author='DevOps @ Kablamo',
    author_email='devops@kablamo.com.au',
    license='MIT',
    packages=['PyStacks'],
    install_requires=[
        'boto3==1.4.7',
        'botocore>=1.8.26',
        'PyYAML==3.12',
        'invoke==0.14.0',
        'Jinja2==2.11.3',
        'pynt==0.8.1',
        'demjson==2.2.3',
        'dnspython==1.15.0',
        'jsonschema==2.6.0',
        'deepdiff==3.3.0',
    ],
    scripts=['bin/pystacks', 'bin/get_pystacks_location.py'],
    zip_safe=False,
)
