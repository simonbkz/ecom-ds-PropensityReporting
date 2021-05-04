import os
from zcrmsdk.src.com.zoho.crm.api.bulk_read import *
from zcrmsdk.src.com.zoho.crm.api.util import Choice


class BulkRead(object):
    @staticmethod
    def create_bulk_read_job(module_api_name):

        """
        This method is used to create a bulk read job to export records.
        :param module_api_name: The API Name of the record's module
        """

        """
        example
        module_api_name = 'Leads'
        """

        # Get instance of BulkReadOperations Class
        bulk_read_operations = BulkReadOperations()

        # Get instance of RequestWrapper Class that will contain the request body
        request = RequestWrapper()

        # Get instance of CallBack Class
        call_back = CallBack()

        # Set valid callback URL
        call_back.set_url("https://www.brightermonday.co.ke")

        # Set the HTTP method of the callback URL. The allowed value is post.
        call_back.set_method(Choice('post'))

        # The Bulk Read Job's details is posted to this URL on successful completion / failure of the job.
        request.set_callback(call_back)

        # Get instance of Query Class
        query = Query()

        # Specifies the API Name of the module to be read.
        query.set_module(module_api_name)

        # Specifies the unique ID of the custom view, whose records you want to export.
        # query.set_cvid('3409643000000087501')

        # List of field names
        field_api_names = ['Converted Leads']

        # Specifies the API Name of the fields to be fetched
        query.set_fields(field_api_names)

        # To set page value, By default value is 1.
        query.set_page(1)

        # Get instance of Criteria Class
        # criteria = Criteria()

        # To set API name of a field
        # criteria.set_api_name('Created Time')

        # To set comparator(eg: equal, greater_than)
        # criteria.set_comparator(Choice('between'))

        # time = ["2020-06-03T17:31:48+05:30", "2020-06-03T17:31:48+05:30"]

        # To set the value to be compared
        # criteria.set_value(time)

        # To filter the records to be exported
        # query.set_criteria(criteria)

        # Set the query object
        request.set_query(query)

        # Specify the value for this key as "ics" to export all records in the Events module as an ICS file.
        # request.set_file_type(Choice('ics'))

        # Call create_bulk_read_job method that takes RequestWrapper instance as parameter
        response = bulk_read_operations.create_bulk_read_job(request)

        if response is not None:
            # Get the status code from response
            print('Status Code: ' + str(response.get_status_code()))

            # Get object from response
            response_object = response.get_object()

            if response_object is not None:

                # Check if expected ActionWrapper instance is received.
                if isinstance(response_object, ActionWrapper):
                    action_response_list = response_object.get_data()

                    for action_response in action_response_list:

                        # Check if the request is successful
                        if isinstance(action_response, SuccessResponse):
                            # Get the Status
                            print("Status: " + action_response.get_status().get_value())

                            # Get the Code
                            print("Code: " + action_response.get_code().get_value())

                            print("Details")

                            # Get the details dict
                            details = action_response.get_details()

                            for key, value in details.items():
                                print(key + ' : ' + str(value))

                            # Get the Message
                            print("Message: " + action_response.get_message().get_value())

                        # Check if the request returned an exception
                        elif isinstance(action_response, APIException):
                            # Get the Status
                            print("Status: " + action_response.get_status().get_value())

                            # Get the Code
                            print("Code: " + action_response.get_code().get_value())

                            print("Details")

                            # Get the details dict
                            details = action_response.get_details()

                            for key, value in details.items():
                                print(key + ' : ' + str(value))

                            # Get the Message
                            print("Message: " + action_response.get_message().get_value())

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
