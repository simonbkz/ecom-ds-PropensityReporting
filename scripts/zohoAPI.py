import os

import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
from zcrmsdk.src.com.zoho.crm.api.user_signature import UserSignature
from zcrmsdk.src.com.zoho.crm.api.dc import USDataCenter
from zcrmsdk.src.com.zoho.api.authenticator.store import FileStore
from zcrmsdk.src.com.zoho.api.logger import Logger
from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
from zcrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken, TokenType
from zcrmsdk.src.com.zoho.crm.api.record import *
from zcrmsdk.src.com.zoho.crm.api import HeaderMap, ParameterMap
from zcrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig

class Record(object):

    def __init__(self):
        pass

    @staticmethod
    def get_records():

        """
        Create an instance of Logger Class that takes two parameters
        1 -> Level of the log messages to be logged. Can be configured by typing Logger.Levels "." and choose any level from the list displayed.
        2 -> Absolute file path, where messages need to be logged.
        """
        logger = Logger.get_instance(level=Logger.Levels.INFO,
                                     file_path="/home/simon/commerce_cube/ecom-ds-PropensityReporting/data/python_sdk_log.log")

        # Create an UserSignature instance that takes user Email as parameter
        user = UserSignature(email="crm+bmke@roam.africa")

        """
        Configure the environment
        which is of the pattern Domain.Environment
        Available Domains: USDataCenter, EUDataCenter, INDataCenter, CNDataCenter, AUDataCenter
        Available Environments: PRODUCTION(), DEVELOPER(), SANDBOX()
        """
        environment = USDataCenter.PRODUCTION()

        """
        Create a Token instance that takes the following parameters
        1 -> OAuth client id.
        2 -> OAuth client secret.
        3 -> REFRESH/GRANT token.
        4 -> token type.
        5 -> OAuth redirect URL.
        """
        token = OAuthToken(client_id=os.getenv("zoho_client_id"), client_secret=os.getenv("zoho_client_secret"),
                           token="1000.974c67913121c5cb15c9d25570be262c.724356476fdb15979aacbee9864cf835",
                           token_type=TokenType.GRANT, redirect_url="https://www.brightermonday.co.ke")# TokenType.GRANT, token=/ GRANT Token

        """
        Create an instance of TokenStore
        1 -> DataBase host name. Default value "localhost"
        2 -> DataBase name. Default value "zohooauth"
        3 -> DataBase user name. Default value "root"
        4 -> DataBase password. Default value ""
        5 -> DataBase port number. Default value "3306"
        """
        store = FileStore(file_path='/home/simon/commerce_cube/ecom-ds-PropensityReporting/data/python_sdk_log.txt')

        """
        auto_refresh_fields (Default value is False)
            if True - all the modules' fields will be auto-refreshed in the background, every hour.
            if False - the fields will not be auto-refreshed in the background. The user can manually delete the file(s) or refresh the fields using methods from ModuleFieldsHandler(zcrmsdk/src/com/zoho/crm/api/util/module_fields_handler.py)

        pick_list_validation (Default value is True)
            A boolean field that validates user input for a pick list field and allows or disallows the addition of a new value to the list.
            if True - the SDK validates the input. If the value does not exist in the pick list, the SDK throws an error.
            if False - the SDK does not validate the input and makes the API request with the user’s input to the pick list
        """
        config = SDKConfig(auto_refresh_fields=True, pick_list_validation=False)

        """
        The path containing the absolute directory path (in the key resource_path) to store user-specific files containing information about fields in modules. 
        """
        resource_path = '/home/simon/commerce_cube/ecom-ds-PropensityReporting/data/'

        """
        Call the static initialize method of Initializer class that takes the following arguments
        1 -> UserSignature instance
        2 -> Environment instance
        3 -> Token instance
        4 -> TokenStore instance
        5 -> SDKConfig instance
        6 -> resource_path
        7 -> Logger instance
        """
        Initializer.initialize(user=user, environment=environment, token=token, store=store, sdk_config=config, resource_path=resource_path, logger=logger)

        try:
            module_api_name = 'Leads'

            param_instance = ParameterMap()

            param_instance.add(GetRecordsParam.converted, 'both')

            # param_instance.add(GetRecordsParam.cvid, '12712717217218')

            header_instance = HeaderMap()

            header_instance.add(GetRecordsHeader.if_modified_since, datetime.now())

            response = RecordOperations().get_records(module_api_name, param_instance, header_instance)

            if response is not None:

                # Get the status code from response
                print('Status Code: ' + str(response.get_status_code()))

                if response.get_status_code() in [204, 304]:
                    print('No Content' if response.get_status_code() == 204 else 'Not Modified')
                    return

                # Get object from response
                response_object = response.get_object()

                if response_object is not None:

                    # Check if expected ResponseWrapper instance is received.
                    if isinstance(response_object, ResponseWrapper):
                        # Get the list of obtained Record instances
                        record_list = response_object.get_data()

                        for record in record_list:

                            # Get the ID of each Record
                            print("Record ID: " + record.get_id())

                            # Get the createdBy User instance of each Record
                            created_by = record.get_created_by()

                            # Check if created_by is not None
                            if created_by is not None:
                                # Get the Name of the created_by User
                                print("Record Created By - Name: " + created_by.get_name())

                                # Get the ID of the created_by User
                                print("Record Created By - ID: " + created_by.get_id())

                                # Get the Email of the created_by User
                                print("Record Created By - Email: " + created_by.get_email())

                            # Get the CreatedTime of each Record
                            print("Record CreatedTime: " + str(record.get_created_time()))

                            if record.get_modified_time() is not None:
                                # Get the ModifiedTime of each Record
                                print("Record ModifiedTime: " + str(record.get_modified_time()))

                            # Get the modified_by User instance of each Record
                            modified_by = record.get_modified_by()

                            # Check if modified_by is not None
                            if modified_by is not None:
                                # Get the Name of the modified_by User
                                print("Record Modified By - Name: " + modified_by.get_name())

                                # Get the ID of the modified_by User
                                print("Record Modified By - ID: " + modified_by.get_id())

                                # Get the Email of the modified_by User
                                print("Record Modified By - Email: " + modified_by.get_email())

                            # Get the list of obtained Tag instance of each Record
                            tags = record.get_tag()

                            if tags is not None:
                                for tag in tags:
                                    # Get the Name of each Tag
                                    print("Record Tag Name: " + tag.get_name())

                                    # Get the Id of each Tag
                                    print("Record Tag ID: " + tag.get_id())

                            # To get particular field value
                            print("Record Field Value: " + str(record.get_key_value('Last_Name')))

                            print('Record KeyValues: ')

                            for key, value in record.get_key_values().items():
                                print(key + " : " + str(value))

                    # Check if the request returned an exception
                    elif isinstance(response_object, APIException):
                        # Get the Status
                        print("Status: " + response_object.get_status().get_value())

                        # Get the Code
                        print("Code: " + response_object.get_code().get_value())

                        print("Details")

                        # Get the details dict
                        details = response_object.get_details()

                        for key, value in details.items():
                            print(key + ' : ' + str(value))

                        # Get the Message
                        print("Message: " + response_object.get_message().get_value())

        except Exception as e:
            print(e)


# logger = Logger.get_instance(level=Logger.Levels.INFO, file_path="~/TokenStore/python_sdk_log.log")
# user = UserSignature(email='crm+bmke@roam.africa')
# environment = USDataCenter.PRODUCTION()
# token = OAuthToken(client_id='1000.B0JO8IFU569FVRS246QRE9QOJGNRPH',
#                    client_secret='4831f8f0895aae2f2d461fc0ab8f06236dfaeed37b',
#                    token='1000.4d4e58a7ac038dfb4be3fab04a9f5907.fcbe7fd6cee65431708de7af6bcca64d',
#                    token_type=TokenType.REFRESH, redirect_url='https://www.brightermonday.co.ke')
# # store = FileStore(file_path='/awethu-test0/TokenStore/python_sdk_tokens.txt')
# config = SDKConfig(auto_refresh_fields=True, pick_list_validation=False)
# resource_path = '~/TokenStore/python-app'
# # Initializer.initialize(user=user, environment=environment, token=token, store=store, resource_path=resource_path, sdk_config=config, logger=logger)