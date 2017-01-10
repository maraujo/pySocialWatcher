# -*- coding: utf-8 -*-
import unittest
from pyfacebookmarketingcrawler.main import PythonFacebookMarketingCrawler
import pyfacebookmarketingcrawler.constants as constants
from pyfacebookmarketingcrawler.utils import *
from testutils import *
import requests


class TestFacebookMarketingCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = PythonFacebookMarketingCrawler
        self.crawler.load_token_file(get_abs_file_path_in_src("tokens.csv"))

    def test_load_tokens_file(self):
        constants.TOKENS = []
        self.assertListEqual(constants.TOKENS, [])
        self.crawler.load_token_file(get_abs_file_path_in_src("facebook_tokens_example.csv"))
        self.assertEqual(len(constants.TOKENS), 2)
        self.assertEqual(constants.TOKENS[0][0], "AEwqewe23ada331asdzxcZXcssdae2qasZCdsr4w5fgdfg56rgfddfSDfSDfasqwq23421123eadadzxwe4234eqdasdsafDwew4ASda231awsad23adczxwe3ADAdadxzd21312sada23dfdBvBHgvhf")
        self.assertEqual(constants.TOKENS[0][1],  "13466789874")

    def test_add_token_and_account_number(self):
        self.crawler.add_token_and_account_number("token", "2312312")
        self.assertEqual(constants.TOKENS[-1], ("token", "2312312"))

    @unittest.skip("Send Request Test Skippied")
    def test_send_request(self):
        response = self.crawler.send_request("http://www.google.com", params={})
        self.assertEqual(response.status_code,200)
        with self.assertRaises(Exception) as context:
            self.crawler.send_request("http://wasdasww.gaasdoogle.casdasdadxzom", params={})
        self.assertTrue(context.exception, RequestException)

    @unittest.skip("Test Behavior List Skipped")
    def test_get_behavior_dataframe(self):
        behavior_dataframe = self.crawler.get_behavior_dataframe()
        behavior_ids = behavior_dataframe["behavior_id"].values
        self.assertTrue("6042330550783" in behavior_ids)
        self.assertTrue("6025000826583" in behavior_ids)
        self.assertTrue("6013017308783" in behavior_ids)

        # @staticmethod
        # def print_behavior_list():
        #     behavior = PythonFacebookMarketingCrawler.get_behavior_list()
        #     behavior.apply(lambda row: pprint.pprint(row), axis=1)


if __name__ == '__main__':
    unittest.main()
