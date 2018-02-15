'''template stuff'''
import os
import json
import demjson
import sys
import output
from jinja2 import Environment, FileSystemLoader


def template(template, **kwargs):
    currentdirectory = os.path.dirname(__file__)

    templatedirectory = os.path.join(
        currentdirectory, '../configs/cftemplates/')
    jinjaenvironment = Environment(
        loader=FileSystemLoader(templatedirectory), trim_blocks=True)

    jinjatemplate = jinjaenvironment.get_template(template + '.json')
    mergedoutput = jinjatemplate.render(kwargs)

    return mergedoutput


def getResources(**kwargs):
    stacks = []
    for i in kwargs['resources']:
        stacks.append(i)
    return stacks


def templateCF(resources, path):
    compiled = {}
    resconf = {}
    for resource in resources:
        resconf[resource] = resources[resource]
        cfres = (template(path + "/" + resource, **resconf))
        try:
            compiled.update(demjson.decode(cfres))
        except demjson.JSONError as err:
            print output.boxwrap(text=cfres)
            print output.writecolour(str(err))
            print err.position
            sys.exit(1)

    return compiled


def voltron(stack, **kwargs):
    ''' form up the cloudformation '''
    conf = kwargs
    cf = {}
    cf['Description'] = conf['description']
    cf['AWSTemplateFormatVersion'] = '2010-09-09'
    cf['Resources'] = templateCF(conf['resources'], 'resources')
    cf['Outputs'] = templateCF(conf['resources'], 'outputs')
    cf['Parameters'] = conf['parameters']
    cf['Mappings'] = conf['mappings']
    return cf


def writecompiled(data, name, region, logoutput=None):

    # Allow for local running from a stacks directory
    local_compiled = os.path.join(os.getcwd(), 'compiled')
    if os.path.exists(local_compiled):
        filedirectory = local_compiled
        targetdirectory = os.path.join(local_compiled, '{region}'.format(region=region))
        path = '{region}/{file}.json'.format(region=region, file=name)
    else:
        filedirectory = os.path.dirname(os.path.realpath(__file__))
        targetdirectory = os.path.join(
            filedirectory, '../configs/user/compiled/{region}/'.format(
                region=region))
        path = '../configs/user/compiled/{region}/{file}.json'.format(
            region=region, file=name)

    if not os.path.exists(targetdirectory):
        os.makedirs(targetdirectory)

    with open(os.path.join(filedirectory, path), "wb") as fh:
        fh.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

    if logoutput:
        print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
