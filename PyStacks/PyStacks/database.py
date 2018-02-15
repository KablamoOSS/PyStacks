import datetime


now = datetime.datetime.now()


class rds:

    def __init__(self, session):
        self.rdsClient = session.client('rds')

    def listDatabases(self):
        databaselist = []
        response = self.rdsClient.describe_db_instances()
        databaselist.extend(response["DBInstances"])
        # while response["Marker"]:
        #     response = self.dnsClient.list_resource_record_sets(
        #         Marker=response["Marker"])
        #     databaselist.extend(response["DBInstances"])
        return databaselist

    def IsMultiAZDatabase(self, instance):
        response = self.rdsClient.describe_db_instances(
            DBInstanceIdentifier=instance)
        return response["DBInstances"]["MultiAZ"]

    def listDatabaseEngine(self, instance):
        response = self.rdsClient.describe_db_instances(
            DBInstanceIdentifier=instance)
        return response["DBInstances"]["Engine"]

    def rebootDatabase(self, instance, failover):
        response = self.rdsClient.reboot_db_instance(
            DBInstanceIdentifier=instance, ForceFailover=failover)
        return response

    def listSnapshots(self, **kwargs):
        databaselist = []
        response = self.rdsClient.describe_db_snapshots(IncludeShared='true')
        databaselist.extend(response["DBSnapshots"])
        while response["Marker"]:
            response = self.dnsClient.list_resource_record_sets(
                Marker=response["Marker"],
                IncludeShared='true')
            databaselist.extend(response["DBSnapshots"])
        return databaselist

    def listSnapshotsbyDB(self, dbinstance, latest=None):
        databaselist = []
        response = self.rdsClient.describe_db_snapshots(
            DBInstanceIdentifier=dbinstance, IncludeShared='true')
        databaselist.extend(response["DBSnapshots"])
        while response["Marker"]:
            response = self.dnsClient.list_resource_record_sets(
                Marker=response["Marker"],
                DBInstanceIdentifier=dbinstance,
                IncludeShared='true')
            databaselist.extend(response["DBSnapshots"])
        # if latest:
        #   youngest = []
        #
        #   for x in databaselist
        #
        # else:
        #    return databaselist

    def changeDatabaseName(self, oldname, newname):
        response = self.rdsClient.modify_db_instance(
            DBInstanceIdentifier=oldname, NewDBInstanceIdentifier=newname)
        return response

    def changeDatabaseMultiAZ(self, name, multiaz):
        response = self.rdsClient.modify_db_instance(
            DBInstanceIdentifier=name, MultiAZ=multiaz)
        return response

    def changeDatabaseSecGroup(self, name, secgroups):
        response = self.rdsClient.modify_db_instance(
            DBInstanceIdentifier=name, DBSecurityGroups=secgroups)
        return response

    def changeDatabaseEngine(self, name, engine):
        response = self.rdsClient.modify_db_instance(
            DBInstanceIdentifier=name, EngineVersion=engine)
        return response

    def changeDatabaseBackupWindow(self, name, window):
        response = self.rdsClient.modify_db_instance(
            DBInstanceIdentifier=name, PreferredBackupWindow=window)
        return response

    def createSnapshot(self, snapshot, instance, tags):
        response = self.rdsClient.create_db_snapshot(
            DBSnapshotIdentifier=snapshot, DBInstanceIdentifier=instance, Tags=[tags])
        return response

    def SnapshotfromResources(self, stackresources):
        for x in stackresources:
            if x['ResourceType'] == "AWS::RDS::DBInstance":
                response = self.rdsClient.create_db_snapshot(
                    DBSnapshotIdentifier=x['PhysicalResourceId'] + "-" + now.isoformat(), DBInstanceIdentifier=x['PhysicalResourceId'])
        return response

    def changeSnapshot(self, snapshot, engine):
        response = self.rdsClient.modify_db_snapshot(
            DBSnapshotIdentifier=snapshot, EngineVersion=engine)
        return response

    def restoreSnapshot(self, instance, snapshot, engine, subnet, securitygroup, tags):
        response = self.rdsClient.restore_db_instance_from_db_snapshot(
            DBClusterIdentifier=instance,
            SnapshotIdentifier=snapshot,
            Engine=engine,
            DBSubnetGroupName=subnet,
            VpcSecurityGroupIds=securitygroup,
            Tags=[tags])
        return response

    def restoreClusterFromSnapshot(self, cluster, snapshot, engine):
        response = self.rdsClient.restore_db_cluster_from_snapshot(
            DBClusterIdentifier=cluster,
            SnapshotIdentifier=snapshot,
            Engine=engine)
        return response

    def listTags(self, arn):
        tagList = []
        response = self.rdsClient.list_tags_for_resource(
            ResourceName=arn,
        )
        tagList.extend(response["TagList"])
        return tagList

    def addTag(self, arn, key, value):
        response = self.rdsClient.add_tags_to_resource(
            ResourceName=arn,
            Tags=[
                {
                    'Key': key,
                    'Value': value
                }
            ]
        )
        return response
