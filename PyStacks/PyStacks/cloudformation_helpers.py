import logging
import os
import cloudformation
import auth
import sys
import yaml


def init_cf_action(parameters, parameters_file, stack_name, region, stack_file):

    parameters_list_from_file = []
    parameters_list_from_args = []

    if parameters_file:
        logging.info('Using passed in parameters for File for Template')
        parameters_list_from_file = load_cf_params_from_file(region, parameters_file)

    if parameters:
        logging.info('Using passed in parameters for CF Template')
        logging.info(parameters)

        parameters_list_from_args = load_cf_params_from_string(parameters)

    parameters_list = parameters_list_from_file + parameters_list_from_args
    logging.info("Parameters to be used for stack: %s" % parameters_list)
    print ("[INFO] Parameters to be used for stack: %s" % parameters_list)

    session, stack_content = get_cf_stack_details(stack_name, region, stack_file)
    cf = cloudformation.stack(session)

    logging.info('Validating Template')

    cf.validate_template_from_file(stack_content=stack_content)

    return cf, stack_content, parameters_list


def final_cf_action(cf, stack_name):
    print "====== Stack Status ======="
    state, status = cf.statusPoller(stackname=stack_name)
    print "============================="
    print "\n"
    print "====== Stack Events History ======="
    display_cf_events(cf.latest_stack_events(stack_name))
    print "============================="
    if state != 0:
        sys.exit(1)
    else:
        resources = cf.getStackResources(stackname=stack_name)
        print "====== Stack Resources ======="
        for resource in resources:
            print "%s -- %s [%s]" % (resource["LogicalResourceId"], resource["PhysicalResourceId"],
                                     resource["ResourceStatus"])
        print "============================="


def handle_cf_error(err):
    logging.error(err)
    if 'does not exist' in str(err):
        print "Stack Removed (or) does not exist"
        sys.exit(1)

    if 'AlreadyExists' in str(err):
        logging.error("Stack Exists")
        sys.exit(1)

    return


def get_cf_stack_details(stack_name, region, stack_file):
    """

    :param stack_name: stack name to create
    :param region: aws region
    :param stack_file: local yaml file
    :return: (aws session, yaml file content)
    """
    stack_content = load_stack_file(stack_file, region)
    authentication = auth.authenticate(region)
    session = authentication.getSession()

    stack_components = stack_name.split('-')
    print "====== Stack Details ======="
    if len(stack_components) == 3:
        print "Project Name: ", stack_components[0]
        print "Application Name: ", stack_components[1]
        print "Stack Suffix: ", stack_components[2]
    print "Region: ", region
    print "Stack YAML File :", stack_file
    print "============================="
    return session, stack_content


def load_stack_file(stack_file, region):
    """
    Validate the yaml file
    :param stack_file: yaml file
    :param region: aps2
    :return:
    """

    directory = os.path.dirname(__file__)
    cf_yaml = '../configs/user/region/{region}/{file}'.format(
        region=region, file=stack_file)

    stack_content = None
    try:
        with open(cf_yaml, "r") as input_file:
            stack_content = input_file.read()
    except IOError as err:
        print 'The file {file} does not exist'.format(file=os.path.join(directory, cf_yaml))
        print(err)
        raise err

    return stack_content


def load_cf_params_from_string(parameters):
    """
    Converts a json string to Cloudformation Parameter/Value pairs.
    :param parameters: string of format 'key1=val1,key2=val2'
    :return: python list of format
    [
        {
            'ParameterKey': 'string',
            'ParameterValue': 'string',
            'UsePreviousValue': True|False
        },
    ]
    """
    cf_param_list = []

    split_params = parameters.split(",")
    for split_param in split_params:
        split_kv = split_param.split("=")
        if split_kv[1] == 'UsePreviousValue':
            cf_param_list.append({'ParameterKey': split_kv[0], 'UsePreviousValue': True})
        else:
            cf_param_list.append({'ParameterKey': split_kv[0], 'ParameterValue': split_kv[1]})

    print "[INFO] Using Parameters from args - %s for stack" % str(cf_param_list)
    return cf_param_list


def display_cf_events(events_array):
    if len(events_array) == 0:
        return False
    status_reason = ""
    for event in events_array:
        if "ResourceStatusReason" in event:
            status_reason = event["ResourceStatusReason"]

        print "%s --> %s - %s ( %s ) ( %s )" % (str(event["Timestamp"]), event["ResourceStatus"],
                                                event["LogicalResourceId"], event["ResourceType"], status_reason)
    return True


def load_cf_params_from_file(region, yaml_file):

    cf_param_list = []
    yaml_file = '../configs/user/region/{region}/{file}'.format(
        region=region, file=yaml_file)
    with open(yaml_file, 'r') as stream:
        data_loaded = yaml.load(stream)

    for k, v in data_loaded.iteritems():
        cf_param_list.append({'ParameterKey': k, 'ParameterValue': v})
    print "[INFO] Adding Parameters fom file %s - %s for stack" % (yaml_file, str(cf_param_list))

    return cf_param_list


def stack_exists(cf, stack_name):
    """

    :param cf:
    :param stack_name:
    :return:
    """
    if not cf.does_stack_exist(stack_name):
        print "ERROR: Stack %s does not exist" % stack_name
        return False

    return True


def get_resources(cf, stack_name, resource_type):
    """

    :param cf:
    :param stack_name:
    :param resource_type:
    :return:
    """

    resources = cf.list_stack_resources(stack_name)
    resource_names = []

    for r in resources:
        if r['ResourceType'] == resource_type:
            r_description = cf.describe_stack_resource(stack_name, r['LogicalResourceId'])
            resource_names.append(r_description["PhysicalResourceId"])

    return resource_names
