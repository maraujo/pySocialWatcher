import main
import logging

watcherAPI = main.PySocialWatcher
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    watcherAPI.load_credentials_file("credentials.csv")
    watcherAPI.check_tokens_account_valid()
    # dataframe = watcherAPI.run_data_collection("input_examples/doha_subregions.json")
    dataframe = watcherAPI.load_data_and_continue_collection("dataframe_collecting_1489064001.csv")