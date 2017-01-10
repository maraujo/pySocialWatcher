# -*- coding: utf-8 -*-
import constants
import requests
import json
import pandas as pd
import pprint
from utils import *


class PythonFacebookMarketingCrawler:
    @staticmethod
    def load_token_file(token_file_path):
        with open(token_file_path, "r") as token_file:
            for line in token_file:
                token = line.split(",")[0].strip()
                account_number = line.split(",")[1].strip()
                constants.TOKENS.append((token, account_number))

    @staticmethod
    def add_token_and_account_number(token,account_number):
        constants.TOKENS.append((token,account_number))

    @staticmethod
    def send_request(url,params):
        try:
            response = requests.get(url, params=params)
        except Exception as error:
            raise RequestException(error.message)
        if response.status_code != 200:
            print response
            raise RequestException(response.content)
        else:
            return response


    @staticmethod
    def get_behavior_dataframe():
        request_payload = {
            'type': 'adTargetingCategory',
            'class': "behaviors",
            'access_token': constants.TOKENS[0][0],
        }
        response = PythonFacebookMarketingCrawler.send_request(constants.GRAPH_SEARCH_URL, request_payload)
        response_content = response.content.encode('utf-8')
        data_json = json.loads(response_content)

        behaviors = pd.DataFrame()
        for entry in data_json["data"]:
            behaviors = behaviors.append({
                "behavior_id": entry["id"],
                "name": entry["name"],
                "description": entry["description"],
                "audience": entry["audience_size"],
                "path": entry["path"]
            }, ignore_index=True)
        return behaviors

    @staticmethod
    def print_behavior_dataframe():
        behavior = PythonFacebookMarketingCrawler.get_behavior_dataframe()
        behavior.apply(lambda row: pprint.pprint(row), axis=1)

    @staticmethod
    def get_interest_id_given_name():
        pass

    @staticmethod
    def print_a_joke():
        print "I used to think the brain was the most important organ.\nThen I thought, look what’s telling me that."
