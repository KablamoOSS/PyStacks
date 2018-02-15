import configs
import kmstasks
import auth
import json


def getConfig(region, stack, githash=None, environment=None, customConfig=None):
    conf = configs.loadConfig(stack, region, githash, environment, customConfig)
    kmsclient = kmstasks.kmstasks()
    authentication = auth.authenticate(conf["region"])
    session = authentication.getSession()
    if 'secrets' in conf:
        conf['secrets'] = kmsclient.decrypt_secrets(session, **conf['secrets'])
        for k, v in conf['secrets'].iteritems():
            param = {'NoEcho': True, 'Description': k, 'Type': 'String', 'Default': v}
            conf['parameters'][k] = param
    return session, conf
