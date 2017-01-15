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


class TestFacebookMarketingCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = PySocialWatcher
        # self.crawler.load_token_file(get_abs_file_path_in_src_folder("tokens.csv"))
        self.crawler.load_token_file(get_abs_file_path_in_src_folder("facebook_tokens_example.csv"))

    def test_load_tokens_file(self):
        constants.TOKENS = []
        self.assertListEqual(constants.TOKENS, [])
        self.crawler.load_token_file(get_abs_file_path_in_src_folder("facebook_tokens_example.csv"))
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

    # @unittest.skip("Test Behavior List Skipped due no tokens")
    def test_get_behavior_dataframe(self):
        behavior_dataframe = self.crawler.get_behavior_dataframe()
        behavior_ids = behavior_dataframe["behavior_id"].values
        self.assertTrue("6042330550783" in behavior_ids)
        self.assertTrue("6025000826583" in behavior_ids)
        self.assertTrue("6013017308783" in behavior_ids)

    # @unittest.skip("Test Interest Given Name Skipped due no tokens")
    def test_get_interest_given_name(self):
        interests_dataframe = self.crawler.get_interests_given_query("obesity")
        interests_names = interests_dataframe["name"].values
        self.assertTrue("Obesity awareness" in interests_names)
        self.assertTrue("Childhood obesity awareness" in interests_names)

    def test_read_json_file(self):
        data_json = self.crawler.read_json_file(get_abs_file_path_in_src_folder("input_examples/example.json"))
        self.assertTrue(type(data_json), type({}))

    def test_build_collection_dataframe(self):
        json_data = self.crawler.read_json_file(get_abs_file_path_in_src_folder("input_examples/quick_example.json"))
        dataframe = self.crawler.build_collection_dataframe(json_data)
        test_dataframe = load_test_dataframe("resources/quick_example_dataframe_skeleton.csv")
        assert_data_frame_almost_equal(dataframe,test_dataframe)

if __name__ == '__main__':
    unittest.main()
