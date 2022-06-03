import json
import boto3
import time
from botocore.exceptions import ClientError
import os


backupVaultName = os.environ['BackupVaultName']
backupPlanName = os.environ['BackupPlanName']
backupSelectionName = os.environ['BackupSelectionName']
backupRuleName = os.environ['RuleName']
scheduleExpression = os.environ['ScheduleExpression']
startWindowMinutes = int(os.environ['StartWindowMinutes'])
completionWindowMinutes = int(os.environ['CompletionWindowMinutes'])
moveToColdStorageAfterDays = int(os.environ['MoveToColdStorageAfterDays'])
deleteAfterDays = int(os.environ['DeleteAfterDays'])
backupPlanTagValue = os.environ['BackupPlanTagValue']
recoveryPointTagValue = os.environ['RecoveryPointTagValue']
kmsKeyARN = os.environ['KmsKeyARN']
backupRoleARN = os.environ['BackupRoleARN']

resourceTagKey = "backupPlan"
resourceTagValue = "12-hrs"
backupName = 'Scheduled_Backup'
backupClient = boto3.client('backup')



def lambda_handler(event, context):
  create_backup_vault(backupVaultName, kmsKeyARN)
  
  BackupPlanId = create_backup_plan(backupPlanName, backupRuleName, backupVaultName, scheduleExpression, startWindowMinutes, completionWindowMinutes, moveToColdStorageAfterDays, deleteAfterDays, recoveryPointTagValue, backupPlanTagValue)

  create_backup_selection(BackupPlanId, backupRoleARN, resourceTagKey, resourceTagValue)



def create_backup_vault(backupVaultName, kmsKeyARN):
  response = backupClient.create_backup_vault(
    BackupVaultName = backupVaultName,
    EncryptionKeyArn = kmsKeyARN,
)

def create_backup_plan(backupPlanName, backupRuleName, backupVaultName, scheduleExpression, startWindowMinutes, completionWindowMinutes, moveToColdStorageAfterDays, deleteAfterDays, recoveryPointTagValue, backupPlanTagValue):
  response = backupClient.create_backup_plan(
    BackupPlan={
        'BackupPlanName': backupPlanName,
        'Rules': [
          {
            'RuleName': backupRuleName,
            'TargetBackupVaultName': backupVaultName,
            'ScheduleExpression': scheduleExpression,
            'StartWindowMinutes': startWindowMinutes,
            'CompletionWindowMinutes': completionWindowMinutes,
            'Lifecycle': {
              'MoveToColdStorageAfterDays': moveToColdStorageAfterDays,
              'DeleteAfterDays': deleteAfterDays
            },
            'RecoveryPointTags': {
              'RuleName': recoveryPointTagValue
            }
          }
        ]
    },
    BackupPlanTags={
        'BackupType': backupPlanTagValue
    }
  )

  BackupPlanId = response['BackupPlanId']
  return BackupPlanId 

def create_backup_selection(BackupPlanId, backupRoleARN, resourceTagKey, resourceTagValue):
  response = backupClient.create_backup_selection(
    BackupPlanId=BackupPlanId,
    BackupSelection={
        'SelectionName': backupSelectionName,
        'IamRoleArn': backupRoleARN,
        # 'Resources': [
        #     'string',
        # ],
        'ListOfTags': [
            {
                'ConditionType': 'STRINGEQUALS',
                'ConditionKey': resourceTagKey,
                'ConditionValue': resourceTagValue
            },
        ],
    },
)
