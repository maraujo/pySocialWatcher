import main
import logging
crawlerAPI = main.PythonFacebookMarketingCrawler
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    crawlerAPI.load_token_file("tokens.csv")
    crawlerAPI.run_data_collection("input_examples/quick_example.json")