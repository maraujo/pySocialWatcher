import main
import logging

watcherAPI = main.PySocialWatcher
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    watcherAPI.load_credentials_file("credentials.csv")
    # watcherAPI.check_tokens_account_valid()
    watcherAPI.run_data_collection("./input_examples/India_test_small_not_scholarities.json")

