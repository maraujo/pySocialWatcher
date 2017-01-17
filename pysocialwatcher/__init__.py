import main
import logging
watcherAPI = main.PySocialWatcher
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    watcherAPI.load_credentials_file("credentials.csv")
    watcherAPI.run_data_collection("input_examples/test_example.json")