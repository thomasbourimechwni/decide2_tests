__author__="tb"

import boto3
from boto3.dynamodb.conditions import Key,Attr
import time

class dynamodb:

    """
        AWS credentials must be set up under /home/"user"/.aws/credentiels
        and /home/"user"/.aws/config
        see : https://boto3.readthedocs.io/en/latest/guide/quickstart.html

    """
    def __init__(self):

        self.writers_number = 5
        self.readers_number = 5
        self.resource = boto3.resource('dynamodb')



if __name__ == '__main__':

        resource = dynamodb().resource
        table = resource.Table('test_earth_input')
        t0 = time.time()
        response = table.scan(
            Limit=20000,
            #FilterExpression=Key('date').between('1431216000000','1432598400000')
        )
        i=0
        total_time = time.time() - t0

        for item in response['Items']:

            print("%s : %s, %s, %s" %(i, item['date'], item['serie_name'], item['value']))
            i+=1

        print("Query executed in %ss" %total_time)

