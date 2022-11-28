import os
import time
import boto3


class AdasEventRepository:
    def __init__(self):
        self._athena = boto3.client('athena')
        self._s3 = boto3.client('s3')

    def get_events(self, device_id: str):
        response = self._athena.start_query_execution(
            QueryString=f"SELECT * FROM adas_event WHERE imei = '{device_id}' LIMIT 10;",
            QueryExecutionContext={
                'Database': 'adas-test'
            },
            ResultConfiguration={
                'OutputLocation': f's3://{os.environ["AWS_S3_BUCKET_QUERY_RESULTS"]}/output/'
            }
        )
        execution_id = response['QueryExecutionId']

        response = self._athena.get_query_execution(QueryExecutionId=execution_id)
        while response['QueryExecution']['Status']['State'] in ['RUNNING', 'QUEUED']:
            time.sleep(3)
            response = self._athena.get_query_execution(QueryExecutionId=execution_id)

        if response['QueryExecution']['Status']['State'] in ['FAILED', 'CANCELLED']:
            print(response)
            raise Exception('Error')

        result_key = execution_id + '.csv'
        self._s3.download_file(f'{os.environ["AWS_S3_BUCKET_QUERY_RESULTS"]}/output/', result_key, 'result.csv')

        print()
