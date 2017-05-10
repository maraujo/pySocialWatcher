from pysocialwatcher import watcherAPI
from multiprocessing import freeze_support

if __name__ == '__main__':
	freeze_support()
	watcher = watcherAPI()
	watcher.load_credentials_file("facebook_credentials_example.csv")
	watcher.run_data_collection("input_examples/quick_example.json")