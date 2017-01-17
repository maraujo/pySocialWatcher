import main
import logging
watcherAPI = main.PySocialWatcher
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    watcherAPI.load_credentials_file("credentials.csv")
    watcherAPI.load_data_and_continue_collection("dataframe_collecting_1484650768.csv")