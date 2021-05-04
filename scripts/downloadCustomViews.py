import os
from zcrmsdk.src.com.zoho.crm.api.user_signature import UserSignature
from zcrmsdk.src.com.zoho.crm.api.dc import USDataCenter
from zcrmsdk.src.com.zoho.api.authenticator.store import DBStore, FileStore
from zcrmsdk.src.com.zoho.api.logger import Logger
from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
from zcrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken, TokenType
from zcrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig
from dotenv import load_dotenv
load_dotenv()

from zcrmsdk.src.com.zoho.crm.api.custom_views import *
from zcrmsdk.src.com.zoho.crm.api import ParameterMap

class CustomView(object):
    @staticmethod
    def get_custom_views(module_api_name):

        """
        Create an instance of Logger Class that takes two parameters
        1 -> Level of the log messages to be logged. Can be configured by typing Logger.Levels "." and choose any level from the list displayed.
        2 -> Absolute file path, where messages need to be logged.
        """
        logger = Logger.get_instance(level=Logger.Levels.INFO,
                                     file_path='/home/simon/commerce_cube/ecom-ds-PropensityReporting/data/python_sdk_log.log')

        # Create an UserSignature instance that takes user Email as parameter
        user = UserSignature(email='crm+bmke@roam.africa')

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
        token = OAuthToken(client_id=os.getenv('zoho_client_id'), client_secret=os.getenv('zoho_client_secret'),
                           token='1000.acf91c67f05293b88835873864375e3b.1183d163705793e2fef0b5fde3241bf7',
                           token_type=TokenType.GRANT, redirect_url='https://www.brightermonday.co.ke')

        """
        Create an instance of TokenStore
        1 -> Absolute file path of the file to persist tokens
        """
        store = FileStore(file_path='/home/simon/commerce_cube/ecom-ds-PropensityReporting/data/python_sdk_tokens.txt')

        """
        Create an instance of TokenStore
        1 -> DataBase host name. Default value "localhost"
        2 -> DataBase name. Default value "zohooauth"
        3 -> DataBase user name. Default value "root"
        4 -> DataBase password. Default value ""
        5 -> DataBase port number. Default value "3306"
        """
        # store = DBStore()
        # store = DBStore(host='host_name', database_name='database_name', user_name='user_name', password='password',port_number='port_number')

        """
        auto_refresh_fields
            if True - all the modules' fields will be auto-refreshed in the background, every hour.
            if False - the fields will not be auto-refreshed in the background. The user can manually delete the file(s) or refresh the fields using methods from ModuleFieldsHandler(zcrmsdk/src/com/zoho/crm/api/util/module_fields_handler.py)

        pick_list_validation
            A boolean field that validates user input for a pick list field and allows or disallows the addition of a new value to the list.
            if True - the SDK validates the input. If the value does not exist in the pick list, the SDK throws an error.
            if False - the SDK does not validate the input and makes the API request with the user’s input to the pick list
        """
        config = SDKConfig(auto_refresh_fields=True, pick_list_validation=False)

        """
        The path containing the absolute directory path (in the key resource_path) to store user-specific files containing information about fields in modules. 
        """
        resource_path = '/home/simon/commerce_cube/ecom-ds-PropensityReporting/data'

        """
        Create an instance of RequestProxy class that takes the following parameters
        1 -> Host
        2 -> Port Number
        3 -> User Name. Default value is None
        4 -> Password. Default value is None
        """
        # request_proxy = RequestProxy(host='proxyHost', port=8080)

        # request_proxy = RequestProxy(host='proxyHost', port=8080, user='userName', password='password')

        """
        Call the static initialize method of Initializer class that takes the following arguments
        1 -> UserSignature instance
        2 -> Environment instance
        3 -> Token instance
        4 -> TokenStore instance
        5 -> SDKConfig instance
        6 -> resource_path
        7 -> Logger instance. Default value is None
        8 -> RequestProxy instance. Default value is None
        """
        Initializer.initialize(user=user, environment=environment, token=token, store=store, sdk_config=config,
                               resource_path=resource_path, logger=logger)

        custom_views_operations = CustomViewsOperations(module_api_name)
        # Call get_custom_view method that takes custom_view_id as parameter
        response = custom_views_operations.get_custom_view(3266912000000087501)
