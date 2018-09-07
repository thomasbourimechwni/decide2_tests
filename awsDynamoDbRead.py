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



    def get_time_for_query(nb_elmnt, table_size):

            resource = dynamodb().resource
            table = resource.Table('test_earth_input_big_table_' + str(table_size))
            t0 = time.time()
            KeyMin= int(table_size/2)
            KeyMax= int(nb_elmnt)
            response = table.scan(
                Limit=10,
                FilterExpression=Key('date').between(int(table_size/2), int((table_size/2)+nb_elmnt))
            )
            i=0
            total_time = time.time() - t0

            for item in response['Items']:

                #print("%s : %s, %s, %s" %(i, item['date'], item['serie_name'], item['value']))
                i+=1

            print("%s %s %s %s %s" %(total_time, 10, table_size, KeyMin, KeyMax))

    list = [10, 100, 1000, 10000,10000, 1000000]

    for i in list:
        get_time_for_query(i, i)

