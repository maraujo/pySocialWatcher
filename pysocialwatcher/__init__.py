import main
import logging
watcherAPI = main.PySocialWatcher
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    watcherAPI.load_credentials_file("credentials.csv")
    watcherAPI.print_geo_locations_given_query_and_location_type("new", ["city"])
    # watcherAPI.check_tokens_account_valid()
    # watcherAPI.run_data_collection("input_examples/quick_example.json")