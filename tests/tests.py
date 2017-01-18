# -*- coding: utf-8 -*-
import unittest
import sys
import imp
try:
    f, filename, description = imp.find_module("pysocialwatcher")
except ImportError:
    f, filename, description = imp.find_module('../pysocialwatcher')
    imp.load_module("pysocialwatcher",f,filename,description)
from pysocialwatcher.main import PySocialWatcher
import pysocialwatcher.constants as constants
from pysocialwatcher.utils import *
from testutils import *
import coverage
import codecov
import pytest_cov
import requests

VALID_TOKENS_PATH = get_abs_file_path_in_src_folder("credentials.csv")
INVALID_TOKENS_PATH = get_abs_file_path_in_src_folder("facebook_credentials_example.csv")

class TestFacebookMarketingCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = PySocialWatcher
        try:
            self.using_valid_tokens = True
            self.crawler.load_credentials_file(VALID_TOKENS_PATH)
        except:
            print "casa"
            self.using_valid_tokens = False
            self.crawler.load_credentials_file(INVALID_TOKENS_PATH)

    # @unittest.skip("Test Get Behaviors Skipped due need valid tokens")
    def test_get_behavior_dataframe(self):
        if not self.using_valid_tokens:
            return
        behavior_dataframe = self.crawler.get_behavior_dataframe()
        behavior_ids = behavior_dataframe["behavior_id"].values
        self.assertTrue("6042330550783" in behavior_ids)
        self.assertTrue("6025000826583" in behavior_ids)
        self.assertTrue("6013017308783" in behavior_ids)

    # @unittest.skip("Test Interest Given Name Skipped due need valid tokens")
    def test_get_interest_given_name(self):
        if not self.using_valid_tokens:
            return
        interests_dataframe = self.crawler.get_interests_given_query("obesity")
        interests_names = interests_dataframe["name"].values
        self.assertTrue("Obesity awareness" in interests_names)
        self.assertTrue("Childhood obesity awareness" in interests_names)

    # @unittest.skip("Test Quick Example Facebook Real Collection Dont Fail Skipped due need valid tokens")
    def test_quick_example_facebook_real_collection_dont_fail(self):
        if not self.using_valid_tokens:
            return
        self.crawler.run_data_collection(get_abs_file_path_in_src_folder("input_examples/quick_example.json"))

    # @unittest.skip("Test Check Tokens Account Valid With Valid Skipped due need valid tokens")
    def test_check_tokens_account_valid_with_valid(self):
        if not self.using_valid_tokens:
            return
        constants.TOKENS = []
        self.crawler.load_credentials_file(VALID_TOKENS_PATH)
        self.crawler.check_tokens_account_valid()

    def test_check_tokens_account_valid_with_invalid(self):
        constants.TOKENS = []
        self.crawler.load_credentials_file(INVALID_TOKENS_PATH)
        with self.assertRaises(Exception) as context:
            self.crawler.check_tokens_account_valid()
        self.assertTrue(context.exception, FatalException)

    def test_load_tokens_file(self):
        constants.TOKENS = []
        self.assertListEqual(constants.TOKENS, [])
        self.crawler.load_credentials_file(get_abs_file_path_in_src_folder("facebook_credentials_example.csv"))
        self.assertEqual(len(constants.TOKENS), 2)
        self.assertEqual(constants.TOKENS[0][0], "AEwqewe23ada331asdzxcZXcssdae2qasZCdsr4w5fgdfg56rgfddfSDfSDfasqwq23421123eadadzxwe4234eqdasdsafDwew4ASda231awsad23adczxwe3ADAdadxzd21312sada23dfdBvBHgvhf")
        self.assertEqual(constants.TOKENS[0][1],  "13466789874")

    def test_add_token_and_account_number(self):
        self.crawler.add_token_and_account_number("token", "2312312")
        self.assertEqual(constants.TOKENS[-1], ("token", "2312312"))

    # @unittest.skip("Send Request Test Skippied")
    def test_send_request(self):
        response = send_request("http://www.google.com", params={})
        self.assertEqual(response.status_code,200)
        with self.assertRaises(Exception) as context:
            send_request("http://wasdasww.gaasdoogle.casdasdadxzom", params={})
        self.assertTrue(context.exception, RequestException)

    def test_read_json_file(self):
        data_json = self.crawler.read_json_file(get_abs_file_path_in_src_folder("input_examples/example.json"))
        self.assertTrue(type(data_json), type({}))

    def test_build_collection_dataframe(self):
        #Testing Quick Example
        json_data = self.crawler.read_json_file(get_abs_file_path_in_src_folder("input_examples/quick_example.json"))
        dataframe = self.crawler.build_collection_dataframe(json_data)
        test_dataframe = load_dataframe_from_file("resources/quick_example_dataframe_skeleton.csv")
        assert_data_frame_almost_equal(dataframe,test_dataframe)
        # Testing Test Example
        json_data = self.crawler.read_json_file(get_abs_file_path_in_src_folder("input_examples/test_example.json"))
        dataframe = self.crawler.build_collection_dataframe(json_data)
        test_dataframe = load_dataframe_from_file("resources/test_example_dataframe_skeleton.csv")
        assert_data_frame_almost_equal(dataframe, test_dataframe)


        # TODO: Tests
        # test_trigger_request_process_and_return_response()
        # test_post_process_collection()
        # select_advance_targeting_type_array_ids with more complex
        # test_get_geo_locations_given_query_and_location_type(query, location_types):
    def tearDown(self):
        constants.TOKENS = []



if __name__ == '__main__':
    unittest.main()
