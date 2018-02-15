import os
import yaml
from jinja2 import Environment, FileSystemLoader


class task:
    def __init__(self, session):
        self.conf = loadServiceConfigs()
        self.ecsClient = session.client('ecs')

    def createContDef(self):
        '''Create Container Definition'''
        containers = []
        for container in self.conf.task['container']:
            contDef = {}
            contDef.update((k, v) for k, v in self.conf.defaults.iteritems() if v is not None)
            contDef.update((k, v) for k, v in container.iteritems() if v is not None)
            containers.append(contDef)
        return containers

    def registerTaskDef(self, contDef, version):
        task = self.ecsClient.register_task_definition(
            family=self.conf.task["family"] + "-" + version,
            containerDefinitions=contDef,
            taskRoleArn=self.conf.task["taskRole"] if self.conf.task[
                "taskRole"] is not None else "",
            volumes=self.conf.task['volumes']
        )
        return task['taskDefinition']['taskDefinitionArn']


class loadServiceConfigs:
    def __init__(self):
        self.task = self.loadFile("user/ecs/task")
        self.defaults = self.loadFile("ecs_defaults/defaults")
        self.deploy = self.loadFile("user/ecs/deploy")

    def loadFile(self, file):
        directory = os.path.dirname(__file__)
        f = open(os.path.join(directory, "../configs/" + file + ".yml"))
        config = yaml.safe_load(f)
        f.close()
        return config


class loadClusterConfigs:
    def __init__(self):
        self.cluster = self.loadFile("user/cluster")

    def loadFile(self, file):
        directory = os.path.dirname(__file__)
        f = open(os.path.join(directory, "../configs/" + file + ".yml"))
        config = yaml.safe_load(f)
        f.close()
        return config


def template_configs(**kwargs):
    directory = os.path.dirname(__file__)
    j2env = Environment(loader=FileSystemLoader(os.path.join(directory, "../configs/user/ecs")), trim_blocks=True)
    for f in os.listdir(os.path.join(directory, "../configs/user/ecs/")):
        templatized = j2env.get_template(f).render(kwargs)
        with open(os.path.join(directory, "../configs/user/ecs/" + f), "wb") as fh:
            fh.write(templatized)


def template_service_cf(taskArn, **kwargs):
    directory = os.path.dirname(__file__)
    j2env = Environment(loader=FileSystemLoader(os.path.join(directory, "../configs/cftemplates/ecs/")), trim_blocks=True)
    f = "ecs_service.json"
    templatized = j2env.get_template(f).render(service=kwargs, TASK_ARN=taskArn)
    return templatized
