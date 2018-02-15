import yaml
import os
import jinja2
import output
import json


def preprocess(env_path, conf_path, region, githash, environment, customParams):
    directory = os.path.dirname(__file__)
    envconfig = None

    with open(os.path.join(directory, env_path), 'r') as f:
        envconfig = yaml.safe_load(f)

    # Ensure the below items are dicts if not exists
    if '_default' not in envconfig.keys():
        envconfig['_default'] = {}
    if environment not in envconfig.keys():
        envconfig[environment] = {}

    if environment:
        context = dict(envconfig['_default'].items() + envconfig[environment].items())  # Append _default to env overwritting
        context['environment'] = environment
    else:
        context = envconfig['_default']

    if githash:
        context['githash'] = githash

    context['region'] = region

    for key, value in customParams.iteritems():
        context[key] = value

    with open(os.path.join(directory, conf_path), 'r') as f:
        jinja_template = jinja2.Template(f.read())
        processed_yaml = jinja_template.render(context)
        config = yaml.safe_load(processed_yaml)

    return config


def loadConfig(file_name, region, githash=None, environment=None, customConfig=None):
    directory = os.path.dirname(__file__)

    env_path = '../configs/user/region/{region}/environment.yml'.format(**locals())
    conf_path = '../configs/user/region/{region}/{file_name}.yml'.format(**locals())

    # Allow running inside a stack config dir without a docker container
    running_in_stack_directory = True
    conf_file = os.path.join(os.getcwd(), 'region/{region}/{file_name}.yml'.format(**locals()))
    if not os.path.exists(conf_file):  # allow to continue as before
        conf_file = os.path.join(directory, conf_path)
        running_in_stack_directory = False

    customParams = {}
    if customConfig:
        try:
            customParams = json.loads(customConfig)
        except:
            print 'error parsing customConfig. Should be valid json'

    config = None
    # If running inside the stack directory, source the environment file locally.
    # If running from a docker container with configs mounted to `configs/user/...`
    if running_in_stack_directory and os.path.isfile(os.path.join(os.getcwd(), 'region/{region}/environment.yml'.format(**locals()))):
        config = preprocess(env_path, conf_path, region, githash, environment, customParams)
    elif not running_in_stack_directory and os.path.isfile(os.path.join(directory, env_path)):
        config = preprocess(env_path, conf_path, region, githash, environment, customParams)
    else:
        try:
            with open(conf_file, 'r') as f:
                config = yaml.safe_load(f)
        except IOError as err:
            print
            print output.piesay(text='The file {file_name} does not exist'.format(file_name=os.path.join(directory, conf_path)))
            print
            raise err

    if 'stackname' not in config:
        raise ValueError('Expected value "stackname" not in template ' + conf_path)

    return config
