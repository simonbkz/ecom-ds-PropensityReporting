from zcrmsdk.src.com.zoho.crm.api.custom_views import *
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

class CustomView(object):
    @staticmethod
    def get_custom_view(module_api_name, custom_view_id):

        """
        This method is used to get the data of any specific custom view of the module with ID
        :param module_api_name: The API name of the required module.
        :param custom_view_id: ID of the CustomView to be obtained
        :return:
        """

        """
        example
        module_api_name = "Leads"
        custom_view_id = 3409643000002955026n
        """

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
                           token='1000.4ceee886d212fe2f4bae575841b2d9d1.8716ba1d1d064921e67612fce4a1cc5b',
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


        # Get instance of CustomViewOperations Class that takes module_api_name as parameter
        custom_views_operations = CustomViewsOperations(module_api_name)

        # Call get_custom_view method that takes custom_view_id as parameter
        response = custom_views_operations.get_custom_view(custom_view_id)

        if response is not None:

            # Get the status code from response
            print('Status Code: ' + str(response.get_status_code()))

            if response.get_status_code() in [204, 304]:
                print('No Content' if response.get_status_code() == 204 else 'Not Modified')
                return

            # Get object from response
            response_object = response.get_object()

            if response_object is not None:

                # Check if expected ResponseWrapper instance is received
                if isinstance(response_object, ResponseWrapper):

                    # Get the list of obtained CustomView instances
                    custom_views_list = response_object.get_custom_views()

                    for custom_view in custom_views_list:

                        # Get the ID of each CustomView
                        print('CustomView ID: ' + str(custom_view.get_id()))

                        # Get the Name of each CustomView
                        print('CustomView Name: ' + str(custom_view.get_name()))

                        # Get the System Name of each CustomView
                        print('CustomView System Name: ' + str(custom_view.get_system_name()))

                        # Get the Category of each CustomView
                        print('CustomView Category: ' + str(custom_view.get_category()))

                        # Get the DisplayValue of each CustomView
                        print('CustomView Display Value: ' + str(custom_view.get_display_value()))

                        # Get the SharedType of each CustomView
                        print('CustomView SharedType: ' + str(custom_view.get_shared_type()))

                        shared_details = custom_view.get_shared_details()

                        if shared_details is not None:
                            for shared_detail in shared_details:
                                # Get the Name of the each SharedDetails
                                print("SharedDetails Name: " + shared_detail.get_name())

                                # Get the ID of the each SharedDetails
                                print("SharedDetails ID: " + shared_detail.get_id())

                                # Get the Type of the each SharedDetails
                                print("SharedDetails Type: " + shared_detail.get_type())

                                # Get the Subordinates of the each SharedDetails
                                print("SharedDetails Subordinates: " + str(shared_detail.get_subordinates()))

                        # Get the Offline value of each CustomView
                        print('CustomView Is offline: ' + str(custom_view.get_offline()))

                        criteria = custom_view.get_criteria()

                        if criteria is not None:
                            CustomView.print_criteria(criteria)

                        # Get the default value of each CustomView
                        print('CustomView Is default: ' + str(custom_view.get_default()))

                        # Get the SortOrder of each CustomView
                        print('CustomView SortBy: ' + str(custom_view.get_sort_by()))

                        if custom_view.get_sort_order() is not None:
                            # Get the SortOrder of each CustomView
                            print('CustomView SortOrder: ' + str(custom_view.get_sort_order()))

                        # Get the SystemDefined of each CustomView
                        print('CustomView Is System Defined: ' + str(custom_view.get_system_defined()))

                        if custom_view.get_favorite() is not None:
                            # Get the Favorite of each CustomView
                            print('CustomView Favorite: ' + str(custom_view.get_favorite()))

                        # Get the fields of each CustomView
                        fields = custom_view.get_fields()

                        if fields is not None:
                            print('Fields')

                            for field in fields:
                                print(field)

                    info = response_object.get_info()

                    if info is not None:
                        print("CustomView Info")

                        translation = info.get_translation()

                        if translation is not None:
                            print("Translation details")

                            # Get the PublicViews of the Translation
                            print('PublicViews: ' + translation.get_public_views())

                            # Get the OtherUsersViews of the Translation
                            print('OtherUsersViews: ' + translation.get_other_users_views())

                            # Get the SharedWithMe of the Translation
                            print('SharedWithMe: ' + translation.get_shared_with_me())

                            # Get the CreatedByMe of the Translation
                            print('CreatedByMe: ' + translation.get_created_by_me())

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

    @staticmethod
    def print_criteria(criteria):

        if criteria.get_comparator() is not None:
            # Get the Comparator of the Criteria
            print('CustomView Criteria Comparator: ' + criteria.get_comparator().get_value())

        if criteria.get_field() is not None:
            # Get the Field of the Criteria
            print('CustomView Criteria Field: ' + criteria.get_field())

        if criteria.get_value() is not None:
            # Get the Value of the Criteria
            print('CustomView Criteria Value: ' + str(criteria.get_value()))

        # Get the List of Criteria instance of each Criteria
        criteria_group = criteria.get_group()

        if criteria_group is not None:
            for each_criteria in criteria_group:
                CustomView.print_criteria(each_criteria)

        if criteria.get_group_operator() is not None:
            # Get the Group Operator of the Criteria
            print('CustomView Criteria Group Operator: ' + criteria.get_group_operator().get_value())