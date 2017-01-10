# -*- coding: utf-8 -*-

import time
UNIQUE_TIME_ID = str(time.time()).split(".")[0]
GRAPH_SEARCH_URL = "https://graph.facebook.com/v2.8/search"
TOKENS = []
MORE1M_USERS_COUNTRIES = ["AE","AF","AL","AO","AR","AT","AU","AZ","BA","BD","BE","BG","BO","BR","CA","CD","CH","CL","CM","CN","CO","CR","CZ","DE","DK","DO","DZ","EC","EG","ES","ET","FI","FR","GB","GE","GH","GR","GT","HK","HN","HR","HT","HU","ID","IE","IL","IN","IQ","IT","JM","JO","JP","KE","KH","KR","KW","KZ","LA","LB","LK","LT","LY","MA","MG","ML","MM","MN","MX","MY","MZ","NG","NI","NL","NO","NP","NZ","OM","PA","PE","PH","PK","PL","PT","PY","QA","RO","RS","RU","SA","SE","SG","SK","SN","SV","TH","TN","TR","TW","TZ","UA","UG","US","UY","VE","VN","YE","ZA","ZM"]
MORE1M_USERS_COUNTRIES_old = ["IN","US","BR","ID","MX","PH","DE","GB","TR","FR","JP","IT","CA","ES","AU","AT","BE","CL","CZ","DK","FI","GR","HU","IE","IL","KR","NL","NZ","NO","PL","PT","SK","SE","CH"]

# OECD Country List
OECD_COUNTRIES = ["US","MX","DE", "GB", "TR", "FR","JP","IT","CA","ES","AU","AT","BE","CL","CZ","DK","EE","FI","GR","HU","IS","IE","IL","KR","LV","LU","NL","NZ","NO","PL","PT","SK","SI","SE","CH"]
# English Spearker Countries
COUNTRIES_ENGLISH = ["US","AU", "NZ", "IE", "IS", "GB", "CA", "PH", "IN"]
# Western Europe Countries https://en.wikipedia.org/wiki/Western_Europe#Population
EUROPE_WESTERN = ["AT","BE","DK","FI","FR","DE","GR","IS", "IE","IT","LU","NL","NO","PT","ES","SE","CH","GB"]
# Too small facebook penetration countries
SMALL_FB_COUNTRIES = ["CN","JP","IN","ID","KR"]
NO_INTEREST_FLAG = "no_interest_selected"


# Example of data_groups structure. Each item in "queries" correspond a one type of experiment that will be runned for  each country.
# DATA_GROUPS = {
#   "queries" :{
#         [{
#             "responses" : [],
#             "requests"  : [],
#             "csv_lines" : [],
#         }],
#     "correlation_lines" : []
#     }
# }

GROUND_TRUTH_COLUMNS = [
    "obesity",
    "high_glucose",
    "alcohol_dependeces",
    "tobacco",
    "war_disease",
    "arab_interests",
    "Pregnant Query Any Text 2"
]
CSV_HEADERS = {
    "data_header" : ["analysis_name","ground_truth_column","country_code","country_name","country_population","country_facebook_population","min_age","max_age","gender","interest","exclusion","placebo","audience","aud_fb_users","bid_amount_median","bid_amount_max","account_budget","pacing_status","dedup_status","bid_amount_min","estimate_DAU","unsupported","cpm_curve_data","cpc_curve_data","reach_max","dedup_winning_rate","reach_min","cpa_curve_data","location","estimate_ready","k=0.001","k=0.05","k=0.5","k=1","k=2","k=3","k=10","k=100","aud_placebo_aud","aud/pla_aud_k=0.001","aud/pla_aud_k=0.05","aud/pla_aud_k=0.5","aud/pla_aud_k=1","aud/pla_aud_k=2","aud/pla_aud_k=3","aud/pla_aud_k=10","aud/pla_aud_k=100","high_glucose","obesity","alcohol_dependeces","tobacco"],
    "correlation_header" : ["interest","exclusion","k=0.001","k=0.05","k=0.5","k=1","k=2","k=3","k=10","k=100","aud/pla_aud_k=0.001","aud/pla_aud_k=0.05","aud/pla_aud_k=0.5","aud/pla_aud_k=1","aud/pla_aud_k=2","aud/pla_aud_k=3","aud/pla_aud_k=10","aud/pla_aud_k=100"]
}
SLEEP_TIME=8
SAVE_THRESHOLD = 300
placebo_index = 0