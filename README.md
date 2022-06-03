# Using AWS Backup & Lambda to Schedule Backups <a id ='top'></a>

<br>
<br>

## Summary

This repo considers multiple approaches to automating backups; using AWS Backup to target resources using tags and using cloudwatch Events to trigger a lambda function that creates a backup

<br>
<br>

## Tech Stack
- AWS CLoudFormation
- AWS Backup
- AWS Lambda
- AWS DynamoDB
- AWS Neptune
- AWS S3

## Architecture Diagram

<details>
<summary> Coming Soon </summary>
<br>

![]()

</details>

<br>
<br>
<br>

# Contents

- [Objective](#obj)
- [Steps](#steps)
- [Via Cloud Formation](#0)
- [Via Terraform](#1)
- [Via CLI/Bash Script](#2)
- [Via Console](#3)
- [Resources](#res)
- [To-Do](#to-do)
- [go to top](#top)

<br>
<br>

# Objective <a id='obj'></a> ([go to top](#top))

## Scenario
Using AWS Backup, schedule the backups of resources tagged with the `Key:backupPlan` and `Value:12-hr` with aws backup. Backups should run at 7am and 7pm daily.

Using Lamda, Schedule the backup of a DynamoDB Table. Backups should run at 7am and 7pm daily.

<br>
<br>
<br>

# Steps <a id='steps'></a> ([go to top](#top))

## Setup Environment
- [ ] Enter `AWS ACCOUNT ID` in [set-env-variable.sh](./scripts/set-env-variables.sh)
- [ ] Enter `STACK NAME` in [set-env-variable.sh](./scripts/set-env-variables.sh)
- [ ] [Opt in to use AWS BackUp](https://docs.aws.amazon.com/aws-backup/latest/devguide/working-with-supported-services.html#working-with-s3#opt-in)
<br>
<br>
<br>

# Via Cloud Formation <a id='0'></a> ([go to top](#top))

<details>
<summary> Expand For Details </summary>

- run
  ```
  export AWS_ACCOUNT_ID="enter account id here"
  export BUCKET_NAME="data-dump-$AWS_ACCOUNT_ID"
  export STACK_NAME="your stack name here"
  chmod u+x ./scripts/deploy-setup.sh
  chmod u+x ./scripts/deploy-aws-backup-yaml.sh
  chmod u+x ./scripts/deploy-aws-backup-lambda.sh
  chmod u+x ./scripts/deploy-event-schedule-lambda.sh
  ```

## AWS Backup

- Deploy the CloudFormation Template [aws-backup.yaml](./1-cloudformation/aws-backup.yaml) by running
  ```
  ./scripts/deploy-aws-backup-yaml.sh update-stack
  ```
  ```
  ./scripts/deploy-aws-backup-yaml.sh delete-stack
  ```

- Or deploy the CloudFormation Template [aws-backup-lambda.yaml](./1-cloudformation/aws-backup-lambda.yaml) by running

  ```
  ./scripts/deploy-aws-backup-lambda.sh update-stack
  ```
  - to invoke the function. 
  ```
  export FUNCTION_NAME="aws-backup-plan-$AWS_ACCOUNT_ID"

  aws lambda invoke \
  --cli-binary-format raw-in-base64-out \
  --payload '{}' \
  --function-name $FUNCTION_NAME \
  $FUNCTION_NAME.json
  ```
  - to delete resources
  ```
  ./scripts/deploy-aws-backup-lambda.sh delete-stack
  ```
  - you would have to delete the backup vault, plan and selection manually, and this mehto created them by invoking a lambda function (aka, i was too lazy to do this myself lol)


## AWS Lambda 

- Deploy the CloudFormation Template [event-schedule-lambda-backup.yaml](1-cloudformation/event-schedule-lambda-backup.yaml) by running

  ```
  ./scripts/deploy-event-schedule-lambda.sh update-stack
  ```
  - to delete resources
  ```
  ./scripts/deploy-event-schedule-lambda.sh delete-stack
  ```
- `You may/will have to delete backups created by lambd fx manually`

## Trigger On Demand Backups

- Files used
  - [CFN Template](./1-cloudformation/on-demand-aws-backup-ddb-table.yaml)
  - [Param File](./1-cloudformation/on-demand-aws-backup-parameters.json)
  - [Python](./lambda/on-demand-aws-backup-ddb-table.py)
  - [bash Script](./scripts/deploy-on-demand-aws-backup-ddb-table.sh)

- To use a cloud watch event to trigger manual aws backups of a ddbtable, run
  ```
  ./scripts/deploy-on-demand-aws-backup-ddb-table.sh update-stack 
  ```
  - to delete resources
  ```
  ./scripts/deploy-on-demand-aws-backup-ddb-table.sh delete-stack 
  ```
- `Note that you will have to delete backups and backup vaults manually`

</details>

<br>
<br>
<br>

# Via Terraform <a id='1'></a> ([go to top](#top))

<details>
<summary> Coming Soon </summary>

</details>

<br>
<br>
<br>

# Via CLI/Bash Script<a id='2'></a> ([go to top](#top))

<details>
<summary> Coming Soon </summary>

</details>

<br>
<br>
<br>

# Via Console <a id='3'></a> ([go to top](#top))

<details>
<summary> Coming Soon </summary>

</details>

<br>
<br>
<br>

# Resources <a id='res'></a> ([go to top](#top))

- [AWS::DynamoDB::Table](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dynamodb-table.html#aws-resource-dynamodb-table-syntax)
- [update-region-settings](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/backup/update-region-settings.html)
- [backup CLI Reference](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/backup/index.html#cli-aws-backup)
- [Creating a backup plan](https://docs.aws.amazon.com/aws-backup/latest/devguide/creating-a-backup-plan.html#plan-cfn)
- [Assign resources to a Backup Plan](https://docs.aws.amazon.com/aws-backup/latest/devguide/assigning-resources.html#assigning-resources-cfn)
- [CFN AWS Backup](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Backup.html)
- [Lambda - Events - DDB backup](https://github.com/awslabs/dynamodb-backup-scheduler) || [Guide](https://aws.amazon.com/blogs/database/a-serverless-solution-to-schedule-your-amazon-dynamodb-on-demand-backup/)
- [Using an AWS CloudFormation Stack to Create a Neptune DB Cluster](https://docs.aws.amazon.com/neptune/latest/userguide/get-started-cfn-create.html)
- [Neptune Boto modify cluster](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/neptune.html#Neptune.Client.modify_db_cluster)
- [CFN Neptune](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Neptune.html)
- [CLI modify Neptune](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/neptune/modify-db-cluster.html)
- [Create Neptune Guide](https://docs.aws.amazon.com/neptune/latest/userguide/get-started-create-cluster.html)
- [Open Search](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html) || [this](https://aws.amazon.com/blogs/aws/amazon-elasticsearch-service-is-now-amazon-opensearch-service-and-supports-opensearch-10/)
- [Boto Open Search](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html)
- [cron schedule expressions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html)
- [DDB Boto](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_backup)
- [Boto AWS BackUp](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/backup.html)
- [Open Search Manual/Automated Backups](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-snapshots.html)
- [link](https://blogs.tensult.com/2020/01/01/aws-lambda-to-perform-various-tasks-in-elasticsearch/)
- [link](https://medium.com/@federicopanini/elasticsearch-backup-snapshot-and-restore-on-aws-s3-f1fc32fbca7f)
- [link](https://medium.com/docsapp-product-and-technology/aws-elasticsearch-manual-snapshot-and-restore-on-aws-s3-7e9783cdaecb)
- [link](https://medium.com/docsapp-product-and-technology/aws-elasticsearch-manual-snapshot-and-restore-on-aws-s3-7e9783cdaecb)
- [link](https://www.elastic.co/guide/en/cloud/current/ec-aws-custom-repository.html)
- [link](https://dev.to/suparnatural/aws-elasticsearch-with-serverless-lambda-2m9b)
- [link](https://john.soban.ski/connect_aws_lambda_to_elasticsearch.html)
- [Backup Open Search](https://www.youtube.com/watch?v=UqoSJYmQLZE&t=1141s)

<br>
<br>
<br>

# To-Do <a id='to-do'></a> ([go to top](#top))

<br>
<br>
<br>



BackupJobId': 'B45CFFE0-84DD-3D20-D928-BEE85E7B0F21', 'RecoveryPointArn': 'arn:aws:backup:us-east-1:526329662628:recovery-point:f742bcc1-c89a-4dad-bac6-b5489542604b', 
BackupJobId': 'B45CFFE0-84DD-3D20-D928-BEE85E7B0F21', 'RecoveryPointArn': 'arn:aws:backup:us-east-1:526329662628:recovery-point:f742bcc1-c89a-4dad-bac6-b5489542604b', 'CreationDate': dateti