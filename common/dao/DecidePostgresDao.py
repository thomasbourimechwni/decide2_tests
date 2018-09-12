#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'tb'
import logging
import sys

from psycopg2.extras import NamedTupleCursor
import pandas as pd
import time
import datetime
from decide2_tests.common.system.LoggingLoader import setup_logging
from decide2_tests.common.dao.ConnectionManager import ConnectionManager
from decide2_tests.common.system.ServiceLoader import ServiceLoader
import json
logger = logging.getLogger("DecideCleaner")

class DecidePostgresDao:

    def __init__(self, connection, logger=None):

        self.conn = connection
        self.cursor = connection.cursor(cursor_factory=NamedTupleCursor)


    def _check_connection(self):
        if self.conn.closed != 0:
            if ServiceLoader.get_level() == "dev_bdd":
                self.conn, self.cursor = ConnectionManager.get_connection("postgres_dev", None)
            if ServiceLoader.get_level() == "prod":
                self.conn, self.cursor = ConnectionManager.get_connection("postgres", None)
            if ServiceLoader.get_level() == "test":
                self.conn, self.cursor = ConnectionManager.get_connection("postgres_test", None)
                #print(ServiceLoader.get_level())

    # sql -d decideint75 -U postgres -c "truncate data_serie_data_prepared;"
    # psql -d decideint75 -U postgres -c "truncate job_list;";
    # psql -d decideint75 -U postgres -c "insert into job_list (job_id) values (0);"
    # psql -d decideint75 -U postgres -c "update job_list set job_status_id = 4 where job_id in (select job_id from job_list where job_status_id != 4);"
    # psql -d decideint75 -U postgres -c "update job_unit set processing = 0 where processing != 0;"
    # psql -d decideint75 -U postgres -c "update project_version set status = 0;

    def insert_points(self):
        self._check_connection()
        try:
            df_all = pd.read_csv('ressources/input.csv', header=0, index_col=['Date'], parse_dates=True, sep=";")
            total = 0
            for column in df_all.columns:
                i=0
                df = df_all[column]


                #print("Importing %s" % df.name)
                t0 = time.time()
                str_json = df.to_json(orient='index',date_format='%Y-%m-%d %H:%M:%S')
                values = json.loads(str_json)
                for key, value in values.items():
                    str_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(key)/1000.))
                    if value is not None:
                        value = format(value, ".15g")

                        self.cursor.execute("insert into points (code, date, value) values ('%s','%s','%s')" %(df.name, str_datetime, value))
                        i+=1
                        total += 1
                total_time = time.time() - t0
                self.conn.commit()
                #print("Import duration with %s writers for %s records and %s items in database was %s" % (self.writers_number, i, count, total_time))
                print("%s;%s;%s" %(total_time, i, total))
                sys.stdout.flush()



        except Exception as e:
            logger.error(e)




    def clean_job_log(self, date_created=None):

        self._check_connection()
        try:
            self.cursor.execute("truncate job_log")
            self.conn.commit()
        except Exception as e:
            logger.error(e)


        logger.info("clean_job_log : truncate job_log")

    def clean_data_serie_data(self, conf_cleaning_point):

        self._check_connection()
        print(conf_cleaning_point)