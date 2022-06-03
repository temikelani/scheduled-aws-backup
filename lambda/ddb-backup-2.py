import datetime
import boto3
import os

#max no of backups to maintain
MAX_BACKUPS = 3

# environmental variables
tableName = os.environ['ddbTableName']
snsArn = os.environ['snsArn']

# boto client
dynamo = boto3.client('dynamodb')
sns = boto3.client('sns')



def lambda_handler(event, context):
  try:
    backup_status = create_backup(tableName)
    if backup_status == 'pass':
      delete_status = delete_old_backups(tableName)
      if delete_status == 'pass':
        sns_success_message()
      else: 
        sns.sns_some_error()
    else:
      sns_fail_message()
  except:
    sns_fail_message()


# create backup function
def create_backup(tableName):
  try:
    print("Backing up table:", tableName)
    backup_name = tableName + '-' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    response = dynamo.create_backup(
        TableName=tableName, BackupName=backup_name)

    print(response)
    print('Backup has been taken successfully for table:', tableName)
    return 'pass'
  except:
    print("Error backing up table.")
    return 'fail'



# delete backup function
def delete_old_backups(tableName):
  try:
    print("Deleting old backups for table:", tableName)

    backups = dynamo.list_backups(TableName=tableName)

    backup_count = len(backups['BackupSummaries'])
    print('Total backup count:', backup_count)

    if backup_count <= MAX_BACKUPS:
        print("No excess backups")
        return 'pass'

    # if backups are greater and MAX_BACKUPS sort backups by creation date
    sorted_list = sorted(backups['BackupSummaries'],key=lambda k: k['BackupCreationDateTime'])
    print(sorted_list)
    old_backups = sorted_list[:MAX_BACKUPS]
    print(old_backups)

    for backup in old_backups:
        arn = backup['BackupArn']
        print("Backup ARN to delete: " + arn)
        deleted_arn = dynamo.delete_backup(BackupArn=arn)
        status = deleted_arn['BackupDescription']['BackupDetails']['BackupStatus']
        print("Status:", status)

    return 'pass'
  
  except:
    print('Error deleting Backups')
    return 'fail'



def sns_success_message():
  response = sns.publish(
    TargetArn = snsArn,
    Message='DynamoDB Backup Successfull',
    Subject='DynamoDB Backup Success' 
  )
  
def sns_fail_message():
  response = sns.publish(
    TargetArn = snsArn,
    Message='DynamoDB Backup Failed',
    Subject='DynamoDB Backup Fail' 
  )

def sns_some_error():
  response = sns.publish(
    TargetArn = snsArn,
    Message='Some error occured',
    Subject='DynamoDB Backup Error' 
  )