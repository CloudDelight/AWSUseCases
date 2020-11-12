################################ README ##############################

Code works on event based triggers and this lambda function will get triggered.

Event bridge set the event sources as per the requirement. this code works if below are the event triggers.

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

Also this is mainly n the event Names and tags are created based on Event Name. 
Here it appends the tags for any modification done.

Tags: Modifiedon 

This will have the time frame as to when the partiv=cular event was done.
