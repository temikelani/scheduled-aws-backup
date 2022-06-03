import json
import boto3
import time
from botocore.exceptions import ClientError
import os

backupVaultName = 'test-1'
startWindowMinutes = 60
completionWindowMinutes = 120
moveToColdStorageAfterDays = 30
deleteAfterDays = moveToColdStorageAfterDays + 90
recoveryPointTagValue = 'on-demand-backup'
kmsKeyARN = 'enter arn'
backupRoleARN = 'enter arn'
ddbTableArn = 'enter arn'

backupClient = boto3.client('backup')

def lambda_handler(event, context):
  if BackupVaultExists() == False:
    createBackUpVault(backupVaultName, kmsKeyARN)
  backupDdbTable(backupVaultName, ddbTableArn, backupRoleARN, startWindowMinutes, completionWindowMinutes, moveToColdStorageAfterDays, deleteAfterDays, recoveryPointTagValue)

def BackupVaultExists():
  backupVaultsList = backupClient.list_backup_vaults().get('BackupVaultList')
  backupVaultNames = [vault.get('BackupVaultName') for vault in backupVaultsList]
  if backupVaultName in backupVaultNames:
    return True
  else:
    return False

def createBackUpVault(backupVaultName, kmsKeyARN):
  response = backupClient.create_backup_vault(
    BackupVaultName = backupVaultName,
    EncryptionKeyArn = kmsKeyARN,
)

def backupDdbTable(backupVaultName, ddbTableArn, backupRoleARN, startWindowMinutes, completionWindowMinutes, moveToColdStorageAfterDays, deleteAfterDays, recoveryPointTagValue):
  response = backupClient.start_backup_job(
    BackupVaultName = backupVaultName,
    ResourceArn = ddbTableArn,
    IamRoleArn = backupRoleARN,
    StartWindowMinutes=startWindowMinutes,
    CompleteWindowMinutes=completionWindowMinutes,
    Lifecycle={
        'MoveToColdStorageAfterDays': moveToColdStorageAfterDays,
        'DeleteAfterDays': deleteAfterDays
    },
    RecoveryPointTags={
        'ddb-backup': recoveryPointTagValue
    }
)

# def backupNeptune(backupVaultName, ddbTableArn, backupRoleARN, startWindowMinutes, completionWindowMinutes, moveToColdStorageAfterDays, deleteAfterDays, recoveryPointTagValue):
#   response = backupClient.start_backup_job(
#     BackupVaultName = backupVaultName,
#     ResourceArn = enter-neptune-arn-here,
#     IamRoleArn = backupRoleARN,
#     IdempotencyToken='string',
#     StartWindowMinutes=startWindowMinutes,
#     CompleteWindowMinutes=completionWindowMinutes,
#     Lifecycle={
#         'MoveToColdStorageAfterDays': moveToColdStorageAfterDays,
#         'DeleteAfterDays': deleteAfterDays
#     },
#     RecoveryPointTags={
#         'ddb-backup': recoveryPointTagValue
#     }
# )


lambda_handler('event', 'context')