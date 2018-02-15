class AutoScaling:

    def __init__(self, session):
        self.as_client = session.client('autoscaling')

    def get_instance_ids_from_auto_scaling_group(self, autoscaling_groups):
        instance_ids = []

        asg_groups_response = self.as_client.describe_auto_scaling_groups(AutoScalingGroupNames=autoscaling_groups)

        for asg_group in asg_groups_response["AutoScalingGroups"]:
            instance_ids += [instance['InstanceId'] for instance in asg_group["Instances"]]
        return instance_ids
