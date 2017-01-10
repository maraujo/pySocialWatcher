import main
crawlerAPI = main.PythonFacebookMarketingCrawler
if __name__ == '__main__':
	crawlerAPI.load_token_file("tokens.csv")
	crawlerAPI.print_behavior_dataframe()
