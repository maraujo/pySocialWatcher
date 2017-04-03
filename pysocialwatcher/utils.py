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
import ast

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

def print_error_warning(error_json, params):
    print_warning("Facebook Error Code: " + str(error_json["error"]["code"]))
    print_warning("Facebook Error Message: " + str(error_json["error"]["message"]))
    if error_json["error"].has_key("error_user_title") and error_json["error"].has_key("error_user_msg"):
        print_warning("Facebook: " + str(error_json["error"]["error_user_title"]) + "\n" + str(
            error_json["error"]["error_user_msg"]))
    print_warning("Facebook Trace Id: " + str(error_json["error"]["fbtrace_id"]))
    print_warning("Request Params : " + str(params))

def get_dataframe_from_json_response_query_data(json_response):
    dataframe = pd.DataFrame()
    for entry in json_response["data"]:
        entry_details = {}
        for field in constants.DETAILS_FIELD_FROM_FACEBOOK_TARGETING_SEARCH:
            entry_details[field] = entry[field] if field in entry else None
        dataframe = dataframe.append(entry_details, ignore_index=True)
    return dataframe

def handle_send_request_error(response, url, params, tryNumber):
    try:
        error_json = json.loads(response.text)
        if error_json["error"]["code"] == constants.API_UNKOWN_ERROR_CODE_1 or error_json["error"]["code"] == constants.API_UNKOWN_ERROR_CODE_2:
            print_error_warning(error_json, params)
            time.sleep(constants.INITIAL_TRY_SLEEP_TIME * tryNumber)
            return send_request(url, params, tryNumber)
        elif error_json["error"]["code"] == constants.INVALID_PARAMETER_ERROR and error_json["error"]["error_subcode"] == constants.FEW_USERS_IN_CUSTOM_LOCATIONS_SUBCODE_ERROR:
            return get_fake_response()
        else:
            logging.error("Could not handle error.")
            raise FatalException(str(error_json["error"]))
    except:
        raise FatalException(str(response.text))

def send_request(url, params, tryNumber = 0):
    tryNumber += 1
    if tryNumber >= constants.MAX_NUMBER_TRY:
        print_warning("Maxium Number of Tries reached. Failing.")
        raise FatalException("Maximum try reached.")
    try:
        response = requests.get(url, params=params)
    except Exception as error:
        raise RequestException(error.message)
    if response.status_code == 200:
        return response
    else:
        return handle_send_request_error(response, url, params, tryNumber)


def call_request_fb(row, token, account):
    target_request = row[constants.TARGETING_FIELD]
    payload = {
        'currency': 'USD',
        'optimize_for': "NONE",
        'targeting_spec': json.dumps(target_request),
        'access_token': token,
    }
    print_info("\tSending in request: {}".format(payload))
    url = constants.REACHESTIMATE_URL.format(account)
    response = send_request(url, payload)
    return response.content

def get_fake_response():
    response = requests.models.Response()
    response._content = constants.FAKE_DATA_RESPONSE_CONTENT
    response.status_code = 200
    logging.warn("Fake Response created: " + response.content)
    return response


def trigger_facebook_call(index, row, token, account, shared_queue):
    try:
        response = call_request_fb(row, token, account)
        shared_queue.put((index, response))
    except RequestException:
        print_warning("Warning Facebook Request Failed")
        print_warning("Row: " + str(row))
        print_warning("It will try again later")
        shared_queue.put((index, numpy.nan))


def add_timestamp(dataframe):
    dataframe["timestamp"] = constants.UNIQUE_TIME_ID
    return dataframe


def add_published_platforms(dataframe, input_json):
    platforms = constants.PUBLISHER_PLATFORM_DEFAULT
    if constants.API_PUBLISHER_PLATFORMS_FIELD in input_json:
        platforms = input_json[constants.API_PUBLISHER_PLATFORMS_FIELD]
    dataframe[constants.API_PUBLISHER_PLATFORMS_FIELD] = json.dumps(platforms)
    return dataframe


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
        raise FatalException("FatalError: Check logging for clue. No way to proceed from here.")


def print_info(message):
    logging.info(message)


def unstrict_literal_eval(string):
    try:
        value = ast.literal_eval(string)
        return value
    except ValueError:
        return string
    except SyntaxError:
        return string


def load_dataframe_from_file(file_path):
    dataframe = pd.DataFrame.from_csv(file_path)
    return dataframe.applymap(unstrict_literal_eval)


def save_response_in_dataframe(shared_queue_list, df):
    for result_tuple in shared_queue_list:
        result_index = result_tuple[0]
        result_response = result_tuple[1]
        df.loc[result_index, "response"] = result_response


def save_skeleton_dataframe(dataframe):
    print_info("Saving Skeleton file: " + constants.DATAFRAME_SKELETON_FILE_NAME)
    dataframe.to_csv(constants.DATAFRAME_SKELETON_FILE_NAME)

def save_temporary_dataframe(dataframe):
    print_info("Saving temporary file: " + constants.DATAFRAME_TEMPORARY_COLLECTION_FILE_NAME)
    dataframe.to_csv(constants.DATAFRAME_TEMPORARY_COLLECTION_FILE_NAME)


def save_after_collecting_dataframe(dataframe):
    print_info("Saving after collecting file: " + constants.DATAFRAME_AFTER_COLLECTION_FILE_NAME)
    dataframe.to_csv(constants.DATAFRAME_AFTER_COLLECTION_FILE_NAME)

def save_after_collecting_dataframe_without_full_response(dataframe):
    dataframe = dataframe.drop('response', 1)
    print_dataframe(dataframe)
    print_info("Saving after collecting file: " + constants.DATAFRAME_AFTER_COLLECTION_FILE_NAME_WITHOUT_FULL_RESPONSE)
    dataframe.to_csv(constants.DATAFRAME_AFTER_COLLECTION_FILE_NAME_WITHOUT_FULL_RESPONSE)


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
            if isinstance(input_data_json[field], list):
                field_content = input_data_json[field]
                to_combine_fields[field] = field_content
            if isinstance(input_data_json[field], dict):
                for intra_field_key in input_data_json[field].keys():
                    to_combine_fields[intra_field_key] = input_data_json[field][intra_field_key]

                # to_combine_fields[field] = build_AND_intra_field_combinations(input_data_json[field])
        except KeyError:
            print_warning("Field not expecified: " + field)

    for field in to_combine_fields.keys():
        for index, value in enumerate(to_combine_fields[field]):
            to_combine_fields[field][index] = (field, value)
    all_combinations = list(itertools.product(*to_combine_fields.values()))
    return all_combinations

def build_AND_intra_field_combinations(intra_field_data):
    intra_fields = []
    for field in intra_field_data.values():
        intra_fields.append(field)
    teste = list(itertools.product(*intra_fields))
    import ipdb;ipdb.set_trace()
    pass



def add_list_of_ANDS_to_input(list_of_ANDS_between_groups,input_data_json):
    for interests_to_AND in list_of_ANDS_between_groups:
        names = []
        and_ors = []
        for interest_to_AND in interests_to_AND:
            names.append(interest_to_AND[constants.INPUT_NAME_FIELD])
            if "or" not in interest_to_AND:
                raise Exception("Only AND of ors are supported")
            and_ors.append(interest_to_AND["or"])
        new_and_interest = {
            constants.INPUT_NAME_FIELD : " AND ".join(names),
            "and_ors" : and_ors,
            "isAND" : True
        }
        input_data_json[constants.INPUT_INTEREST_FIELD].append(new_and_interest)


def generate_collection_request_from_combination(current_combination, input_data):
    targeting = build_targeting(current_combination,input_data)
    dataframe_row = {}
    for field in current_combination:
        field_name = field[0]
        value = field[1]
        dataframe_row[field_name] = value
    dataframe_row[constants.ALLFIELDS_FIELD] = current_combination
    dataframe_row[constants.TARGETING_FIELD] = targeting
    dataframe_row[constants.INPUT_NAME_FIELD] = input_data[constants.INPUT_NAME_FIELD]
    return dataframe_row


def select_common_fields_in_targeting(targeting, input_combination_dictionary):
    # Selecting Geolocation
    geo_location = input_combination_dictionary[constants.INPUT_GEOLOCATION_FIELD]
    if geo_location.has_key(constants.INPUT_GEOLOCATION_LOCATION_TYPE_FIELD):
        location_type = geo_location[constants.INPUT_GEOLOCATION_LOCATION_TYPE_FIELD]
    else:
        location_type = constants.DEFAULT_GEOLOCATION_LOCATION_TYPE_FIELD

    targeting[constants.API_GEOLOCATION_FIELD] = {
        geo_location["name"]: geo_location["values"],
        constants.INPUT_GEOLOCATION_LOCATION_TYPE_FIELD: location_type
    }
    # Selecting Age
    age_range = input_combination_dictionary[constants.INPUT_AGE_RANGE_FIELD]
    targeting[constants.API_MIN_AGE_FIELD] = age_range[constants.MIN_AGE] if age_range.has_key(constants.MIN_AGE) else None
    targeting[constants.API_MAX_AGE_FIELD] = age_range[constants.MAX_AGE] if age_range.has_key(constants.MAX_AGE) else None

    # Selecting genders
    gender = input_combination_dictionary[constants.INPUT_GENDER_FIELD]
    targeting[constants.API_GENDER_FIELD] = [gender]

    # Selecting Languages
    if input_combination_dictionary.has_key(constants.INPUT_LANGUAGE_FIELD):
        languages = input_combination_dictionary[constants.INPUT_LANGUAGE_FIELD]
        if languages:
            targeting[constants.API_LANGUAGES_FIELD] = languages["values"]
    else:
        print_warning("No field: " + constants.INPUT_LANGUAGE_FIELD)


def get_api_field_name(field_name):
    return constants.INPUT_TO_API_FIELD_NAME[field_name]


def process_audience_from_response(literal_response):
    audience = json.loads(literal_response)["data"]["users"]
    return int(audience)


def post_process_collection(collection_dataframe):
    # For now just capture audience
    print_info("Computing Audience column")
    collection_dataframe["audience"] = collection_dataframe["response"].apply(
        lambda x: process_audience_from_response(x))
    return collection_dataframe


def select_advance_targeting_type_array_ids(segment_type, input_value, targeting):
    api_field_name = get_api_field_name(segment_type)
    if input_value:
        if input_value.has_key("or"):
            or_query = []
            for or_id in input_value["or"]:
                or_query.append({"id" : or_id})
            targeting["flexible_spec"].append({api_field_name: or_query})

        if input_value.has_key("and"):
            for id_and in input_value["and"]:
                targeting["flexible_spec"].append({segment_type: {"id" : id_and}})

        if input_value.has_key("not"):
            if not "exclusions" in targeting:
                targeting["exclusions"] = {}
            if not api_field_name in targeting["exclusions"].keys():
                targeting["exclusions"][api_field_name] = []
            for id_not in input_value["not"]:
                targeting["exclusions"][api_field_name].append({"id" : id_not})

        if input_value.has_key("and_ors"):
            for or_ids in input_value["and_ors"]:
                or_query = []
                for or_id in or_ids:
                    or_query.append({"id" : or_id})
                targeting["flexible_spec"].append({segment_type: or_query})

        if not input_value.has_key("or") and not input_value.has_key("and") and not input_value.has_key("not") and not input_value.has_key("and_ors"):
            raise JsonFormatException("Something wrong with: " + str(input_value))


def get_interests_by_group_to_AND(input_data_json, groups_ids):
    interests_by_group_to_AND = {}
    for group_id in groups_ids:
        interests_by_group_to_AND[group_id] = []
    for interest_input in input_data_json[constants.INPUT_INTEREST_FIELD]:
        if interest_input:
            if constants.GROUP_ID_FIELD in interest_input:
                interest_group_id = interest_input[constants.GROUP_ID_FIELD]
                if interest_group_id in interests_by_group_to_AND:
                    interests_by_group_to_AND[interest_group_id].append(interest_input)
    return interests_by_group_to_AND

def select_advance_targeting_type_array_integer(segment_type, input_value, targeting):
    api_field_name = get_api_field_name(segment_type)
    if input_value:
        try:
            targeting["flexible_spec"].append({api_field_name : input_value["or"]})
        except:
            raise JsonFormatException("Something wrong with: " + str(input_value))


def select_advance_targeting_fields(targeting, input_combination_dictionary):
    # Selecting Advance Targeting
    targeting["flexible_spec"] = []

    for advance_field in constants.ADVANCE_TARGETING_FIELDS_TYPE_ARRAY_IDS:
        if input_combination_dictionary.has_key(advance_field):
            select_advance_targeting_type_array_ids(advance_field, input_combination_dictionary[advance_field], targeting)
    for advance_field in constants.ADVANCE_TARGETING_FIELDS_TYPE_ARRAY_INTEGER:
        if input_combination_dictionary.has_key(advance_field):
            select_advance_targeting_type_array_integer(advance_field, input_combination_dictionary[advance_field], targeting)
    return targeting


def select_publisher_platform(targeting, input_data):
    # Selecting Publisher Platform
    platform = constants.PUBLISHER_PLATFORM_DEFAULT
    if constants.API_PUBLISHER_PLATFORMS_FIELD in input_data:
        platform = input_data[constants.API_PUBLISHER_PLATFORMS_FIELD]
    targeting[constants.API_PUBLISHER_PLATFORMS_FIELD] = platform

def build_targeting(current_combination, input_data):
    targeting = {}
    input_combination_dictionary = dict(current_combination)
    select_common_fields_in_targeting(targeting, input_combination_dictionary)
    select_advance_targeting_fields(targeting, input_combination_dictionary)
    select_publisher_platform(targeting, input_data)
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
def send_dumb_query(token, account):
    try:
        row = pd.Series()
        row[constants.TARGETING_FIELD] = constants.DEFAULT_DUMB_TARGETING
        call_request_fb(row, token, account)
    except Exception as error:
        print_warning("Token or Account Number Error:")
        print_warning("Token:" + token)
        print_warning("Account:" + account)
        raise  error


