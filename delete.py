import boto3
import json
import os
import datetime

#Only for Local Tests
def localtest():
    boto3.setup_default_session(profile_name='XXX')
    DAYS_TO_KEEP = 101
    VAULT_NAME = 'XXX'
    deletebackups(VAULT_NAME, DAYS_TO_KEEP)

def lambda_handler(event, context):
    DAYS_TO_KEEP = int(os.environ['DAYS_TO_KEEP'])
    VAULT_NAME = os.environ['VAULT_NAME']
    deletebackups(VAULT_NAME, DAYS_TO_KEEP)

def deletebackups(vaultname, daystokeep):
    creation_date = datetime.datetime.combine( datetime.date.today() - datetime.timedelta(days=daystokeep), datetime.datetime.min.time())
    print('Selecting Recovery Points created after {0}'.format(creation_date))
    client = boto3.client('backup')
    response = client.list_recovery_points_by_backup_vault(
        BackupVaultName=vaultname,
        ByCreatedBefore=creation_date
    )

    for rp in response['RecoveryPoints']:
        rparn = rp['RecoveryPointArn']
        print ('Deleting: {0}'.format(rparn))
        try:
            deleteresponse = client.delete_recovery_point(
                BackupVaultName=vaultname,
                RecoveryPointArn=rparn
            )
            if (deleteresponse['ResponseMetadata']['HTTPStatusCode'] == 200):
                print("OK")
        except Exception as e:
            print(e)

localtest()