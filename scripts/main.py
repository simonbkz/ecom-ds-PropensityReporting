import pandas as pd
# import numpy as np
from AllLeads import MapAllLeads
# from zohoAPI import Record
# from downloadResults import BulkRead as dBulkRead
# from zohoBulkAPI import *
# from initializeSDK import SDKInitializer
from CustomViews import CustomView
from downloadCustomViews import CustomView as dCustomViews
from getCustomView import CustomView as CustomView1
# from downloadResults import BulkReadOperations
# import json
import boto3
import os

def format_data(query_allLeads,
                queryAllDeals):

    map = MapAllLeads(query_allLeads,
                queryAllDeals)
    map.processDealsAndLeads()

if __name__ == '__main__':

    client = boto3.client("s3",
                          aws_access_key_id = os.getenv("aws_access_key_id"),
                          aws_secret_access_key = os.getenv("aws_secret_access_key"))
    # Record.get_records()
    # SDKInitializer.initialize()
    # BulkRead.create_bulk_read_job('Leads')

    # f = open(
    #     '/home/simon/commerce_cube/ecom-ds-PropensityReporting/data/resources/Y3JtK2Jta2VodHRwczovL3d3dy56b2hvYXBpcy5jb20=.json',
    #     'r')
    # d = json.loads(f.read())
    # deals = None
    # for i in d['deals']:
    #     deals = pd.DataFrame(i
    # v = pd.DataFrame(d)
    # bulk_read_operations = BulkReadOperations()
    # response = bulk_read_operations.download_result(3266912000103164047)
    # dBulkRead()
    # CustomView.get_custom_views('Leads')
    dCustomViews.get_custom_views("Leads")
    #TODO: all leads that have been uploaded, see how many appear in the deals table within x period

    # CustomView1.get_custom_view("Leads",3266912000000087501)
    bucket_name = "prod-ritdu-ecom-data"
    allLeadsScriptKey = "propensity/data/reporting/input/allLeads.txt"
    allDealsScriptKey = "propensity/data/reporting/input/allDeals.txt"
    allLeads_obj = client.get_object(Bucket=bucket_name, Key=allLeadsScriptKey)
    allLeads_query_body = allLeads_obj[u'Body']
    query_allLeads = allLeads_query_body.read().decode('utf-8').split()

    allDeals_obj = client.get_object(Bucket=bucket_name, Key=allDealsScriptKey)
    allDeals_query_body = allDeals_obj[u'Body']
    query_allDeals = allDeals_query_body.read().decode('utf-8').split()

    format_data(query_allLeads,query_allDeals)
