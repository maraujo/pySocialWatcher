import main
import logging
watcherAPI = main.PySocialWatcher
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    watcherAPI.load_token_file("tokens.csv")
    watcherAPI.run_data_collection("input_examples/quick_example.json")