# -*- coding: utf-8 -*-
import sys


from utils import *


class PySocialWatcher:
    @staticmethod
    def load_credentials_file(token_file_path):
        with open(token_file_path, "r") as token_file:
            for line in token_file:
                token = line.split(",")[0].strip()
                account_number = line.split(",")[1].strip()
                PySocialWatcher.add_token_and_account_number(token, account_number)

    @staticmethod
    def add_token_and_account_number(token,account_number):
        constants.TOKENS.append((token,account_number))

    @staticmethod
    def get_search_targeting_from_query_dataframe(query):
        token, account_id = get_token_and_account_number_or_wait()
        request_payload = {
            'q': query,
            'access_token': token
        }
        response = send_request(constants.TARGETING_SEARCH_URL.format(account_id), request_payload)
        json_response = load_json_data_from_response(response)
        dataframe_response = get_dataframe_from_json_response_query_data(json_response)
        return dataframe_response

    @staticmethod
    def get_behavior_dataframe():
        request_payload = {
            'type': 'adTargetingCategory',
            'class': "behaviors",
            'access_token': get_token_and_account_number_or_wait()[0]
        }
        response = send_request(constants.GRAPH_SEARCH_URL, request_payload)
        json_response = load_json_data_from_response(response)
        behaviors_dataframe = get_dataframe_from_json_response_query_data(json_response)
        return behaviors_dataframe

    @staticmethod
    def get_interests_given_query(interest_query):
        request_payload = {
            'type': 'adinterest',
            'q': interest_query,
            'access_token': get_token_and_account_number_or_wait()[0]
        }
        response = send_request(constants.GRAPH_SEARCH_URL, request_payload)
        json_response = load_json_data_from_response(response)
        interests_dataframe = get_dataframe_from_json_response_query_data(json_response)
        return interests_dataframe

    @staticmethod
    def get_geo_locations_given_query_and_location_type(query, location_types):
        request_payload = {
            'type': 'adgeolocation',
            'location_types': location_types,
            'q': query,
            'access_token': get_token_and_account_number_or_wait()[0]
        }
        response = send_request(constants.GRAPH_SEARCH_URL, request_payload)
        json_response = load_json_data_from_response(response)
        locations_dataframe = get_dataframe_from_json_response_query_data(json_response)
        return locations_dataframe

    @staticmethod
    def print_search_targeting_from_query_dataframe(query):
        search_dataframe = PySocialWatcher.get_search_targeting_from_query_dataframe(query)
        print_dataframe(search_dataframe)

    @staticmethod
    def print_geo_locations_given_query_and_location_type(query, location_types):
        geo_locations = PySocialWatcher.get_geo_locations_given_query_and_location_type(query, location_types)
        print_dataframe(geo_locations)

    @staticmethod
    def print_interests_given_query(interest_query):
        interests = PySocialWatcher.get_interests_given_query(interest_query)
        print_dataframe(interests)

    @staticmethod
    def print_behaviors_list():
        behaviors = PySocialWatcher.get_behavior_dataframe()
        print_dataframe(behaviors)

    @staticmethod
    def read_json_file(file_path):
        file_ptr = open(file_path, "r")
        json_file_raw = file_ptr.read()
        file_ptr.close()
        try:
            json_data = json.loads(json_file_raw)
        except ValueError as error:
            raise JsonFormatException(error.message)
        return json_data

    @staticmethod
    def build_collection_dataframe(input_data_json):
        print_info("Building Collection Dataframe")
        collection_dataframe = build_initial_collection_dataframe()
        collection_queries = []
        input_combinations = get_all_combinations_from_input(input_data_json)
        print_info("Total API Requests:" + str(len(input_combinations)))
        for index,combination in enumerate(input_combinations):
            print_info("Completed: {0:.2f}".format(100*index/float(len(input_combinations))))
            collection_queries.append(generate_collection_request_from_combination(combination, input_data_json))
        dataframe = collection_dataframe.append(collection_queries)
        dataframe = add_timestamp(dataframe)
        dataframe = add_published_platforms(dataframe, input_data_json)
        if constants.SAVE_EMPTY:
            dataframe.to_csv(constants.DATAFRAME_SKELETON_FILE_NAME)
        save_skeleton_dataframe(dataframe)
        return dataframe

    @staticmethod
    def perform_collection_data_on_facebook(collection_dataframe):
        # Call each requests builded
        processed_rows_after_saved = 0
        dataframe_with_uncompleted_requests = collection_dataframe[pd.isnull(collection_dataframe["response"])]
        while not dataframe_with_uncompleted_requests.empty:
            print_collecting_progress(dataframe_with_uncompleted_requests, collection_dataframe)
            # Trigger requests
            rows_to_request = dataframe_with_uncompleted_requests.head(len(constants.TOKENS))
            responses_list = trigger_request_process_and_return_response(rows_to_request)
            # Save response in collection_dataframe
            save_response_in_dataframe(responses_list, collection_dataframe)
            processed_rows_after_saved += len(responses_list)
            # Save a temporary file
            if processed_rows_after_saved >= constants.SAVE_EVERY:
                save_temporary_dataframe(collection_dataframe)
                processed_rows_after_saved = 0
            # Update not_completed_experiments
            dataframe_with_uncompleted_requests = collection_dataframe[pd.isnull(collection_dataframe["response"])]
        print_info("Data Collection Complete")
        save_temporary_dataframe(collection_dataframe)
        post_process_collection(collection_dataframe)
        save_after_collecting_dataframe(collection_dataframe)
        return collection_dataframe

    @staticmethod
    def check_tokens_account_valid():
        print_info("Testing tokens and account number")
        for token, account in constants.TOKENS:
            send_dumb_query(token, account)
        print_info("All tokens and respective account number are valid.")

    @staticmethod
    def check_input_integrity(input_data_json):
        # Check input has name propertity
        if not constants.INPUT_NAME_FIELD in input_data_json:
            raise FatalException("Input should have key: " + constants.INPUT_NAME_FIELD)
        # Check if every field in input is supported
        for field in input_data_json.keys():
            if not field in constants.ALLOWED_FIELDS_IN_INPUT:
                raise FatalException("Field not supported: " + field)

    @staticmethod
    def expand_input_if_requested(input_data_json):
        if constants.PERFORM_AND_BETWEEN_GROUPS_INPUT_FIELD in input_data_json:
            for groups_ids in input_data_json[constants.PERFORM_AND_BETWEEN_GROUPS_INPUT_FIELD]:
                interests_by_group_to_AND = get_interests_by_group_to_AND(input_data_json,groups_ids)
                list_of_ANDS_between_groups = list(itertools.product(*interests_by_group_to_AND.values()))
                add_list_of_ANDS_to_input(list_of_ANDS_between_groups, input_data_json)

    @staticmethod
    def run_data_collection(json_input_file_path):
        input_data_json = PySocialWatcher.read_json_file(json_input_file_path)
        PySocialWatcher.expand_input_if_requested(input_data_json)
        PySocialWatcher.check_input_integrity(input_data_json)
        collection_dataframe = PySocialWatcher.build_collection_dataframe(input_data_json)
        collection_dataframe = PySocialWatcher.perform_collection_data_on_facebook(collection_dataframe)
        return collection_dataframe

    @staticmethod
    def load_data_and_continue_collection(input_file_path):
        collection_dataframe = load_dataframe_from_file(input_file_path)
        collection_dataframe = PySocialWatcher.perform_collection_data_on_facebook(collection_dataframe)
        return collection_dataframe

    @staticmethod
    def config(sleep_time = 8, save_every = 300, save_after_empty_dataframe = False):
        constants.SLEEP_TIME = sleep_time
        constants.SAVE_EVERY = save_every
        constants.SAVE_EMPTY = save_after_empty_dataframe

    @staticmethod
    def print_bad_joke():
        print "I used to think the brain was the most important organ.\nThen I thought, look what’s telling me that."
