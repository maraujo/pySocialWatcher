# -*- coding: utf-8 -*-
import json
from tabulate import tabulate
import pandas as pd
import constants
import itertools
import logging
import coloredlogs
import time
from multiprocessing import Process, Manager
import numpy
import requests
import traceback
import sys

coloredlogs.install(level=logging.INFO)

class RequestException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class JsonFormatException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class FatalException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def send_request(url, params):
    try:
        response = requests.get(url, params=params)
    except Exception as error:
        raise RequestException(error.message)
    if response.status_code == 200:
        return response
    else:
        if response.status_code >= 400 and response.status_code <= 499:
            error_json = json.loads(response.text)
            print_warning("Facebook Error Code: " + str(error_json["error"]["code"]))
            print_warning("Facebook Error Message: " + str(error_json["error"]["message"]))
            if error_json["error"].has_key("error_user_title") and error_json["error"].has_key("error_user_msg"):
                print_warning("Facebook: " + str(error_json["error"]["error_user_title"]) + "\n" + str(error_json["error"]["error_user_msg"]))
            print_warning("Facebook Trace Id: " + str(error_json["error"]["fbtrace_id"]))
            raise FatalException(str(error_json["error"]["message"]))
        else:
            raise FatalException(str(response.text))


def call_request_fb(target_request, token, account):
    payload = {
        'currency': 'USD',
        'optimize_for': "OFFSITE_CONVERSIONS",
        'targeting_spec': json.dumps(target_request),
        'access_token': token
    }
    print_info("\tSending in request: {}".format(payload))
    url = constants.REACHESTIMATE_URL.format(account)
    response = send_request(url,payload)
    return response.content


def trigger_facebook_call(index, row, token, account, shared_queue):
    try:
        response = call_request_fb(row[constants.TARGETING_FIELD], token, account)
        shared_queue.put((index, response))
    except RequestException:
        print_warning("Warning Facebook Request Failed")
        print_warning("Row: " + str(row))
        print_warning("It will try again later")
        shared_queue.put((index, numpy.nan))



def trigger_request_process_and_return_response(rows_to_request):
    process_manager = Manager()
    shared_queue = process_manager.Queue()
    shared_queue_list = []
    list_process = []

    # Trigger Process in rows
    for index, row in rows_to_request.iterrows():
        token, account = get_token_and_account_number_or_wait()
        p = Process(target=trigger_facebook_call, args=(index, row, token, account, shared_queue))
        list_process.append(p)

    # Starting process
    map(lambda p: p.start(), list_process)
    # Stop process
    map(lambda p: p.join(), list_process)
    #Check for Exception
    map(lambda p: check_exception(p), list_process)

    # Put things from shared list to normal list
    while shared_queue.qsize() != 0:
        shared_queue_list.append(shared_queue.get())
    return shared_queue_list


def check_exception(p):
    if p.exitcode != 0:
        raise FatalException("Fatar Error: Check stacktrace for clue. No way to proceed from here.")

def print_info(message):
    logging.info(message)


def save_response_in_dataframe(shared_queue_list, df):
    for result_tuple in shared_queue_list:
        result_index = result_tuple[0]
        result_response = result_tuple[1]
        df.loc[result_index, "response"] = result_response


def save_temporary_dataframe(dataframe):
    print_info("Saving temporary file")
    dataframe.to_csv(constants.DATAFRAME_TEMPORARY_COLLECTION_FILE_NAME)


def save_after_collecting_dataframe(dataframe):
    print_info("Saving after collecting file: " + constants.DATAFRAME_AFTER_COLLECTION_FILE_NAME)
    dataframe.to_csv(constants.DATAFRAME_AFTER_COLLECTION_FILE_NAME)


def print_warning(message):
    logging.warn(message)


def load_json_data_from_response(response):
    response_content = response.content.encode('utf-8')
    return json.loads(response_content)


def print_dataframe(df):
    print tabulate(df, headers='keys', tablefmt='psql', floatfmt=".0f")


def build_initial_collection_dataframe():
    return pd.DataFrame(columns= constants.DATAFRAME_COLUMNS)


def get_all_combinations_from_input(input_data_json):
    to_combine_fields = {}
    for field in constants.INPUT_FIELDS_TO_COMBINE:
        try:
            to_combine_fields[field] = input_data_json[field]
        except KeyError:
            print_warning("Field not expecified: " + field)

    for field in to_combine_fields.keys():
        for index, value in enumerate(to_combine_fields[field]):
            to_combine_fields[field][index] = (field, value)
    all_combinations = list(itertools.product(*to_combine_fields.values()))
    return all_combinations


def generate_collection_request_from_combination(combination, name):
    targeting = build_targeting(combination)
    dataframe_row = {}
    for field in combination:
        field_name = field[0]
        value = field[1]
        dataframe_row[field_name] = value
    dataframe_row[constants.ALLFIELDS_FIELD] = combination
    dataframe_row[constants.TARGETING_FIELD] = targeting
    dataframe_row[constants.INPUT_NAME_FIELD] = name
    return dataframe_row


def select_common_fields_in_targeting(targeting, input_dictionary):
    # Selecting Countries
    country = input_dictionary[constants.INPUT_LOCATION_FIELD]
    targeting["geo_locations"] = {
        "countries": [country],
        "location_types": ["home"]  # TODO: make this changeble
    }
    # Selecting Age
    age_range = input_dictionary[constants.INPUT_AGE_RANGE_FIELD]
    targeting[constants.API_MIN_AGE_FIELD] = age_range[constants.MIN_AGE] if age_range.has_key(constants.MIN_AGE) else None
    targeting[constants.API_MAX_AGE_FIELD] = age_range[constants.MAX_AGE] if age_range.has_key(constants.MAX_AGE) else None

    # Selecting genders
    gender = input_dictionary[constants.INPUT_GENDER_FIELD]
    targeting[constants.API_GENDER_FIELD] = [gender]

    # Selecting Languages
    if input_dictionary.has_key(constants.INPUT_LANGUAGE_FIELD):
        languages = input_dictionary[constants.INPUT_LANGUAGE_FIELD]
        if languages:
            targeting[constants.API_LANGUAGES_FIELD] = languages["or"]
    else:
        print_warning("No field: " + constants.INPUT_LANGUAGE_FIELD)


def get_api_field_name(field_name):
    return constants.INPUT_TO_API_FIELD_NAME[field_name]


def select_advance_targeting_type_array_ids(field_name, input_value, targeting):
    api_field_name = get_api_field_name(field_name)
    if input_value:
        if input_value.has_key("or"):
            or_query = []
            for or_value in input_value["or"]:
                or_query.append({"id" : or_value})
            targeting["flexible_spec"].append({api_field_name: or_query})
        elif input_value.has_key("and"):
            for and_item in input_value["and"]:
                targeting["flexible_spec"].append({"id": and_item})
        elif input_value.has_key("not"):
            targeting["exclusions"][api_field_name] = []
            for not_item in input_value["not"]:
                targeting["exclusions"][api_field_name].append(not_item)
        else:
            raise JsonFormatException("Something wrong with: " + str(input_value))


def select_advance_targeting_type_array_integer(field_name, input_value, targeting):
    api_field_name = get_api_field_name(field_name)
    if input_value:
        try:
            targeting["flexible_spec"].append({api_field_name : input_value["or"]})
        except:
            raise JsonFormatException("Something wrong with: " + str(input_value))


def select_advance_targeting_fields(targeting, input_dictionary):
    # Selecting Advance Targeting
    targeting["flexible_spec"] = []
    targeting["exclusions"] = {}

    for advance_field in constants.ADVANCE_TARGETING_FIELDS_TYPE_ARRAY_IDS:
        if input_dictionary.has_key(advance_field):
            select_advance_targeting_type_array_ids(advance_field, input_dictionary[advance_field], targeting)
    for advance_field in constants.ADVANCE_TARGETING_FIELDS_TYPE_ARRAY_INTEGER:
        if input_dictionary.has_key(advance_field):
            select_advance_targeting_type_array_integer(advance_field, input_dictionary[advance_field], targeting)
    return targeting


def build_targeting(input_combination):
    targeting = {}
    input_dictionary = dict(input_combination)
    select_common_fields_in_targeting(targeting, input_dictionary)
    select_advance_targeting_fields(targeting, input_dictionary)
    return targeting


def get_token_and_account_number_or_wait():
    if not "used_tokens_time_map" in globals():
        global used_tokens_time_map
        used_tokens_time_map = {}
    while True:
        for token, account in constants.TOKENS:
            if used_tokens_time_map.has_key(token):
                last_used_time = used_tokens_time_map[token]
                time_since_used = time.time() - last_used_time
                if time_since_used > constants.SLEEP_TIME:
                    used_tokens_time_map[token] = time.time()
                    return token, account
            else:
                used_tokens_time_map[token] = time.time()
                return token, account
        time.sleep(1)


def print_collecting_progress(uncomplete_df, df):
    full_size = len(df)
    uncomplete_df_size = len(uncomplete_df)
    print_info("Collecting... Completed: {:.2f}% , {:d}/{:d}".format((float(full_size - uncomplete_df_size) / full_size * 100),
                                                                     full_size - uncomplete_df_size, full_size))



