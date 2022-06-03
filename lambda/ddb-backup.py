from __future__ import print_function
from datetime import date, datetime, timedelta
from botocore.exceptions import ClientError

import json
import boto3
import time
import os

ddbRegion = os.environ['AWS_DEFAULT_REGION']
tableName = os.environ['DDBTable']
backupName = 'Scheduled_Backup'

MIN_BACKUPS = 3 # min no of backups to trigger delete
ddb = boto3.client('dynamodb', region_name=ddbRegion)
print('Backup started for: ', backupName)

# for deleting old backup. It will search for old backup and will escape deleting last backup days you mentioned in the backup retention
#backupRetentionDays=2
backupRetentionDays = int(os.environ['BackupRetention']) # less tha 35
retentionThreshold = backupRetentionDays-1


def lambda_handler(event, context):
  latestBackupCount = create_backup(tableName, backupName)
  delete_old_backups(tableName, latestBackupCount, backupName)
		
def create_backup(ddbTable, backupName):
  try:
  #create backup
    ddb.create_backup(TableName = ddbTable, BackupName = backupName)
    print('Backup has been taken successfully for table:', ddbTable)
    
    #check recent backup
    fromDate = datetime.now() - timedelta(days=retentionThreshold)
    latestDate = datetime.now()

    listBackupsResponse = ddb.list_backups(
      TableName=ddbTable, 
      TimeRangeLowerBound=datetime(fromDate.year, fromDate.month, fromDate.day), 
      TimeRangeUpperBound=datetime(latestDate.year, latestDate.month, latestDate.day)
    )
    
    latestBackupCount=len(listBackupsResponse['BackupSummaries'])
    print('Total backup count in recent days:',latestBackupCount)
    return latestBackupCount
  except  ClientError as e:
    print(e)
  except ValueError as ve:
    print('error:',ve)
  except Exception as ex:
    print(ex)


def delete_old_backups(ddbTable,latestBackupCount, backupName):
  try: 
    # check if there are any backups before backupRetentionDays days go
    latestDate = datetime.now() - timedelta(days=backupRetentionDays)
    print(latestDate)

		# TimeRangeLowerBound is the release of Amazon DynamoDB Backup and Restore - Nov 29, 2017
		backupsBeyondRetention = ddb.list_backups(
      TableName=ddbTable,
      TimeRangeLowerBound=datetime(2017, 11, 29),
      TimeRangeUpperBound=datetime(latestDate.year, latestDate.month, latestDate.day)
    )
		
		#check that you have at least MIN_BACKUPS amount of backups
		if latestBackupCount >= MIN_BACKUPS:
			if 'LastEvaluatedBackupArn' in backupsBeyondRetention:
				lastEvalBackupArn = backupsBeyondRetention['LastEvaluatedBackupArn']
			else:
				lastEvalBackupArn = ''
			
			while (lastEvalBackupArn != ''):
				for record in backupsBeyondRetention['BackupSummaries']:
					backupArn = record['BackupArn']
					ddb.delete_backup(BackupArn=backupArn)
					print(backupName, 'has deleted this backup:', backupArn)

				response = ddb.list_backups(
          TableName=ddbTable,
          TimeRangeLowerBound=datetime(2017, 11, 23),
          TimeRangeUpperBound=datetime(deleteupperDate.year, deleteupperDate.month, deleteupperDate.day),
          ExclusiveStartBackupArn=lastEvalBackupArn
        )

				if 'LastEvaluatedBackupArn' in response:
					lastEvalBackupArn = response['LastEvaluatedBackupArn']
				else:
					lastEvalBackupArn = ''
					print ('the end')
		else:
			print ('Recent backup does not meet the deletion criteria')
  except  ClientError as e:
		print(e)

	except ValueError as ve:
		print('error:',ve)
	
	except Exception as ex:
		print(ex)