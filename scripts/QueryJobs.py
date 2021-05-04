import pandas as pd
# from decouple import config
import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

class QueryJobs():

    def __init__(self,
                 data_extract_fname):
        self.data_extract_fname = data_extract_fname

    def getData(self):

        # These have to match what we defined here: https://github.com/RingierIMU/ritdu-ecom/blob/master/infra/release.tf#L25
        db_host = os.getenv('RDS_HOST_jobs')
        db_name = os.getenv('RDS_DB_NAME_jobs')
        db_user = os.getenv('RDS_USERNAME')
        db_password = os.getenv('RDS_PASSWORD')


        table_name = ""
        # print("table_name has been initialized")
        connection = pymysql.connect(host=db_host,
                                     db=db_name,
                                     user=db_user,
                                     password=db_password,
                                     charset="utf8mb4",
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            cursor = connection.cursor()

            # check processes on commerce rds

            sql = """select COUNT(*)
                    from INFORMATION_SCHEMA.PROCESSLIST
                    where state = 'executing'"""

            cursor.execute(sql)
            # process_count = cursor.fetchone()
            # print("Connection has been successfully setup:")
            print("\nExecuting second query")
            # sql = """{0}""".format(self.queryString)
            # sql_query = pd.read_csv(self.data_extract_fname,sep="\n",header=None)[0].str.cat()
            cursor.execute(self.data_extract_fname)
            table_name = cursor.fetchall()

        except Exception as e:

            print("Exeception occured:{}".format(e))

        finally:

            cursor.close()
            # connection.commit()
            connection.close()
            print("DB Connection closed")

        df = pd.DataFrame(table_name)
        return df