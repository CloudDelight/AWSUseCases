from __future__ import print_function
from botocore.exceptions import ClientError
import json
import boto3
import logging
import time
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    #logger.info('Event: ' + str(event))
    #print('Received event: ' + json.dumps(event, indent=2))

    #Declarations
    key = 'event'
    ids = []
    resourceId = ''
    resourceArn = ''
    resourceName = ''
    currentTime = datetime.now(tz=timezone.utc).strftime("%d/%m/%Y %H:%M:%S") + " - UTC"

    #FunctionDefinition
    def EC2Tag():
        if not detail['requestParameters']:
            logger.warning('Not requestParameters found')
            if detail['errorCode']:
                logger.error('errorCode: ' + detail['errorCode'])
            if detail['errorMessage']:
                logger.error('errorMessage: ' + detail['errorMessage'])
            return False


        ec2 = boto3.resource('ec2')

        if eventName == 'RebootInstances':
            items = detail['requestParameters']['instancesSet']['items']
            for item in items:
                ids.append(item['instanceId'])               
        elif eventName == 'StopInstances':
            items = detail['requestParameters']['instancesSet']['items']
            for item in items:
                ids.append(item['instanceId'])
        elif eventName == 'ModifyInstanceAttribute':
            ids.append(detail['requestParamaters']['instanceId'])
        elif eventName == 'DeleteNetworkInterface':
            ids.append(detail['requestParameters']['networkInterfaceId'])
        elif eventName == 'DetachVolume':
            ids.append(detail['requestParameters']['volumeId'])
        elif eventName == 'ModifyVolume':
            ids.append(detail['requestParameters']['ModifyVolumeRequest']['VolumeId'])
        elif eventName == 'AuthorizeSecurityGroupIngress':
            ids.append(detail['requestParameters']['groupId'])
        elif eventName == 'ModifyNetworkInterfaceAttribute':
            ids.append(detail['requestParameters']['networkInterfaceId'])
        elif eventName == 'ModifySubnetAttribute':
            ids.append(detail['requestParameters']['subnetId'])
        elif eventName == 'RevokeSecurityGroupEgress':
            ids.append(detail['requestParameters']['groupId'])
        elif eventName == 'ModifyVpcAttribute':
            ids.append(detail['requestParameters']['vpcId'])
        elif eventName == 'DisassociateVpcCidrBlock':
            ids.append(detail['requestParameters']['vpcId'])
        elif eventName == 'ModifyTransitGateway':
            ids.append(detail['requestParameters']['transitGatewayId'])
        else:
            logger.warning('Not supported action')
        
       
        if ids:
            for resourceid in ids:
                logger.info('Tagging resource ' + str(resourceid))

            ec2.create_tags(Resources=ids, Tags=[{'Key': 'modifiedon', 'Value': currentTime}])

        logger.info('Remaining time (ms): ' + str(context.get_remaining_time_in_millis()) + '\n')
        return True

    def AutoscalingGroupTag():
        if not detail['requestParameters']:
            logger.warning('Not requestParameters found')
            if detail['errorCode']:
                logger.error('errorCode: ' + detail['errorCode'])
            if detail['errorMessage']:
                logger.error('errorMessage: ' + detail['errorMessage'])
            return False
    
        autoscaling = boto3.client('autoscaling')

        if eventName == 'UpdateAutoScalingGroup':
            resourceName = detail['requestParameters']['autoScalingGroupName']
        elif eventName == 'SuspendProcesses':
            resourceName = detail['requestParameters']['autoScalingGroupName']
        else:
            logger.warning('Not supported action')

        if resourceName:
            logger.info('Tagging resource ' + str(resourceName))

            autoscaling.create_or_update_tags(Tags=[
                {
                    'ResourceId': resourceName,
                    'ResourceType': 'auto-scaling-group',
                    'Key': 'modifiedon',
                    'Value': currentTime
                }
            ])

        logger.info('Remaining time (ms): ' + str(context.get_remaining_time_in_millis()) + '\n')
        return True

    def EMRTag():
        if not detail['requestParameters']:
            logger.warning('Not requestParameters found')
            if detail['errorCode']:
                logger.error('errorCode: ' + detail['errorCode'])
            if detail['errorMessage']:
                logger.error('errorMessage: ' + detail['errorMessage'])
            return False

        emr = boto3.client('emr')

        if eventName == 'ModifyInstanceGroups':
            resourceId = (detail['requestParameters']['instanceGroups']['instanceGroupId'])
        elif eventName == 'SetVisibleToAllUsers':
            resourceId = (detail['requestParameters']['jobFlowIds'])
        else:
            logger.warning('Not supported action')

        if resourceId:
            logger.info('Tagging resource ' + str(resourceId))

            response = emr.add_tags(
                ResourceId=resourceId,
                Tags=[
                    {
                        'Key': 'modifiedon',
                        'Value': currentTime
                    }
                ]
            )

        logger.info('Remaining time (ms): ' + str(context.get_remaining_time_in_millis()) + '\n')
        return True


    def SagemakerTag():
        if not detail['requestParameters']:
            logger.warning('Not requestParameters found')
            if detail['errorCode']:
                logger.error('errorCode: ' + detail['errorCode'])
            if detail['errorMessage']:
                logger.error('errorMessage: ' + detail['errorMessage'])
            return False

        sagemaker = boto3.client('sagemaker')

        if eventName == 'StopNotebookInstance':
            resourceName = detail(['requestParameters']['notebookInstanceName'])
        elif eventName == 'UpdateNotebookInstance':
            resourceName = detail(['requestParameters']['notebookInstanceName'])
    
        else:
            logger.warning('Not supported action')

        if resourceName:
            logger.info('Tagging resource ' + str(resourceName))

            response = sagemaker.add_tags(
                ResourceName = resourceName,
                Tags=[
                    {
                        'Key': 'modifiedon',
                        'Value': currentTime
                    }
                ]
            )

        logger.info('Remaining time (ms): ' + str(context.get_remaining_time_in_millis()) + '\n')
        return True

    def RedshiftTag():
        if not detail['responseElements']:
            logger.warning('Not responseElements found')
            if detail['errorCode']:
                logger.error('errorCode: ' + detail['errorCode'])
            if detail['errorMessage']:
                logger.error('errorMessage: ' + detail['errorMessage'])
            return False

        redshift = boto3.client('redshift')

        if eventName == 'RebootCluster':
            resourceName = detail(['responseElements']['clusterIdentifier'])
        elif eventName == 'PauseCluster':
            resourceName = detail(['responseElements']['clusterIdentifier'])
        elif eventName == 'ModifyCluster':
            resourceName = detail(['responseElements']['clusterIdentifier'])
        else:
            logger.warning('Not supported action')

        if resourceName:
            logger.info('Tagging resource ' + str(resourceName))

            response = redshift.create_tags(
                ResourceName=resourceName,
                Tags=[
                    {
                        'Key': 'modifiedon',
                        'Value': currentTime
                    }
                ]
            )

        logger.info('Remaining time (ms): ' + str(context.get_remaining_time_in_millis()) + '\n')
        return True

    def RDSTag():
        if not detail['requestParameters']:
            logger.warning('Not requestParameters found')
            if detail['errorCode']:
                logger.error('errorCode: ' + detail['errorCode'])
            if detail['errorMessage']:
                logger.error('errorMessage: ' + detail['errorMessage'])
            return False

        rds = boto3.client('rds')

        if eventName == 'StopDBCluster':
            resourceName = detail['requestParameters']['dBClusterIdentifier']
        elif eventName == 'ModifyDBCluster':
            resourceName = detail['responseElements']['dBClusterIdentifier']
        
        else:
            logger.warning('Not supported action')
            
    
        
        if resourceName:
            logger.info('Tagging resource ' + str(resourceName))

            response = rds.add_tags_to_resource(
                ResourceName=resourceName,
                Tags=[
                    {
                        'Key': 'modifiedon',
                        'Value': currentTime
                    }
                ]
            )

        logger.info('Remaining time (ms): ' + str(context.get_remaining_time_in_millis()) + '\n')
        return True

    try:
        if key in event:
            detail = event['event']['detail']
        else:
            detail = event['detail']

        if detail:
            region = event['region']
            eventName = detail['eventName']
            eventSource = detail['eventSource']

            logger.info('region: ' + str(region))
            logger.info('eventName: ' + str(eventName))

            if eventSource == 'ec2.amazonaws.com':
                EC2Tag()
            elif eventSource == 'autoscaling.amazonaws.com':
                AutoscalingGroupTag()
            elif eventSource == 'dax.amazonaws.com' or eventSource == 'dynamodb.amazonaws.com':
                DynamoDBTag()
            elif eventSource == 'elasticmapreduce.amazonaws.com':
                EMRTag()
            elif eventSource == 'sagemaker.amazonaws.com':
                SagemakerTag()
            elif eventSource == 'rds.amazonaws.com':
                RDSTag()
            elif eventSource == 'redshift.amazonaws.com':
                RedshiftTag()

    except Exception as e:
        logger.error('Something went wrong: ' + str(e))
        return False
