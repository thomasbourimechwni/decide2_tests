__author__="tb"

import boto3
import pandas as pd
import json
import time
from boto3.dynamodb.table import BatchWriter

class dynamodb:

    """
        AWS credentials must be set up under /home/"user"/.aws/credentiels
        and /home/"user"/.aws/config
        see : https://boto3.readthedocs.io/en/latest/guide/quickstart.html

    """
    def __init__(self):
        self.writers_number = 60
        self.dynamodb = boto3.resource('dynamodb')

    def create_table(self):

        table = self.dynamodb.create_table(
            TableName='users',
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'last_name',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'last_name',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': self.writers_number
            }
        )

        table.meta.client.get_waiter('table_exists').wait(TableName='users')
        print(table.item_count)

    def create_table_for_massive_test(self, number_of_elements):
        table_name = 'test_earth_input_big_table_%s' %number_of_elements
        table = self.dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'serie_name',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'date',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'serie_name',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'date',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': self.writers_number
            }
        )

        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)


    def get_table_info(self):

        table = self.dynamodb.Table('users')
        print(table.creation_date_time)

    def add_item(self):

        table = self.dynamodb.Table('users')
        item={
            'username':'jonedoe',
            'first_name':'jane',
            'last_name': 'Doe',
            'age':25,
            'account_type':'standard_user',  
        }
        table.put_item(Item=item)

    def get_item(self):
        table = self.dynamodb.Table('users')
        response = table.get_item(Key={'username':'janedoe', 'last_name':'Doe'})
        item = response['Item']

    def massive_insert(self):
        sizes=[10,100,1000,10000,100000,1000000]

        for size in sizes:
            self.create_table_for_massive_test(size)
            print("time;nb of writers;inserted items")
            table = self.dynamodb.Table('test_earth_input_big_table_%s' %size)
            batch = BatchWriter(table_name= 'test_earth_input_big_table_%s' %size,client=table.meta.client, flush_amount=25)
            t0 = time.time()
            for i in range (0, size):
                    item = {'serie_name': 'MYSERIE',
                            'date': str(i),
                            'value': i}
                    batch.put_item(Item=item)
            total_time = time.time() - t0
            print("%s;%s;%s" %(total_time, self.writers_number, i))




    # with table.batch_writer() as batch:
        #     for column in df_all.columns:
        #         i=0
        #         df = df_all[column]
        #         #print("Importing %s" % df.name)
        #         count = self.get_items_number(table) #outside of time calculation loop for accuracy
        #         t0 = time.time()
        #         str_json = df.to_json(orient='index')
        #         values = json.loads(str_json)
        #         for key, value in values.items():
        #             if value is not None:
        #                 item = {'serie_name': df.name,
        #                         'date': key,
        #                         'value': format(value, ".15g")}
        #                 batch.put_item(Item=item)
        #                 i+=1
        #
        #         total_time = time.time() - t0
        #
        #         #print("Import duration with %s writers for %s records and %s items in database was %s" % (self.writers_number, i, count, total_time))
        #         print("%s;%s;%s;%s" %(total_time, self.writers_number, i, count))

    def get_table_desc(self, table):
        dynamoDBClient = boto3.client('dynamodb')
        table_description = dynamoDBClient.describe_table(
            TableName=table)
        return table_description

    def get_items_number(self, table):

        data = table.scan()

        return data['Count']


    #def get_json_from_csvrow(self, row):

if __name__ == '__main__':

    dynamodb_test = dynamodb()
    #dynamodb_test.create_table()
    #dynamodb_test.add_item()
    #dynamodb_test.get_item()
    #dynamodb_test.create_table_for_massive_test()
    dynamodb_test.massive_insert()


