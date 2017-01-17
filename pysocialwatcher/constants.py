# -*- coding: utf-8 -*-
import time
SAVE_EMPTY = False
SLEEP_TIME = 8
SAVE_EVERY = 300
NUMBER_OF_REQUESTS_PER_BUCKET = 100
UNIQUE_TIME_ID = str(time.time()).split(".")[0]
DATAFRAME_SKELETON_FILE_NAME = "dataframe_skeleton_" + UNIQUE_TIME_ID + ".csv"
DATAFRAME_TEMPORARY_COLLECTION_FILE_NAME = "dataframe_collecting_" + UNIQUE_TIME_ID + ".csv"
DEFAULT_DUMB_TARGETING = {'geo_locations': {u'regions': [{u'key': u'3843'}], 'location_types': ['home']}, 'genders': [0], }
DATAFRAME_AFTER_COLLECTION_FILE_NAME = "collect_finished_" + UNIQUE_TIME_ID + ".csv"
REACHESTIMATE_URL = "https://graph.facebook.com/v2.8/act_{}/reachestimate"
GRAPH_SEARCH_URL = "https://graph.facebook.com/v2.8/search"
TOKENS = []
INPUT_AGE_RANGE_FIELD = "ages_ranges"
INPUT_GEOLOCATION_FIELD = "geo_locations"
INPUT_GEOLOCATION_LOCATION_TYPE_FIELD = "location_types"
DEFAULT_GEOLOCATION_LOCATION_TYPE_FIELD = ["home"]
INPUT_GENDER_FIELD = "genders"
INPUT_INTEREST_FIELD = "interests"
INPUT_BEHAVIOR_FIELD = "behavior"
INPUT_SCHOLARITY_FIELD = "scholarities"
INPUT_LANGUAGE_FIELD = "languages"
INPUT_FAMILYSTATUS_FIELD = "family_statuses"
TARGETING_FIELD = "targeting"
RESPONSE_FIELD = "response"
AUDIENCE_FIELD = "audience"
ALLFIELDS_FIELD = "all_fields"
INPUT_NAME_FIELD = "name"
MIN_AGE = "min"
MAX_AGE = "max"

API_INTEREST_FIELD = "interests"
API_BEHAVIOR_FIELD = "behaviors"
API_SCHOLARITY_FIELD = "education_statuses"
API_FAMILYSTATUS_FIELD = "family_statuses"
API_LANGUAGES_FIELD = "locales"
API_GENDER_FIELD = "genders"
API_MIN_AGE_FIELD = "age_min"
API_MAX_AGE_FIELD = "age_max"
API_GEOLOCATION_FIELD = "geo_locations"

DATAFRAME_COLUMNS = [
            INPUT_NAME_FIELD,
            INPUT_AGE_RANGE_FIELD,
            INPUT_GEOLOCATION_FIELD,
            INPUT_GENDER_FIELD,
            INPUT_INTEREST_FIELD,
            INPUT_BEHAVIOR_FIELD,
            INPUT_SCHOLARITY_FIELD,
            INPUT_LANGUAGE_FIELD,
            INPUT_FAMILYSTATUS_FIELD,
            ALLFIELDS_FIELD,
            TARGETING_FIELD,
            RESPONSE_FIELD,
            AUDIENCE_FIELD
        ]

INPUT_FIELDS_TO_COMBINE = [
    INPUT_INTEREST_FIELD,
    INPUT_AGE_RANGE_FIELD,
    INPUT_GENDER_FIELD,
    INPUT_BEHAVIOR_FIELD,
    INPUT_SCHOLARITY_FIELD,
    INPUT_LANGUAGE_FIELD,
    INPUT_FAMILYSTATUS_FIELD,
    INPUT_GEOLOCATION_FIELD
]

ADVANCE_TARGETING_FIELDS_TYPE_ARRAY_IDS = [
    INPUT_INTEREST_FIELD,
    INPUT_BEHAVIOR_FIELD,
    INPUT_FAMILYSTATUS_FIELD,
]

ADVANCE_TARGETING_FIELDS_TYPE_ARRAY_INTEGER = [
    INPUT_SCHOLARITY_FIELD
]

INPUT_TO_API_FIELD_NAME = {
    INPUT_GENDER_FIELD : API_GENDER_FIELD,
    INPUT_INTEREST_FIELD: API_INTEREST_FIELD,
    INPUT_BEHAVIOR_FIELD: API_BEHAVIOR_FIELD,
    INPUT_SCHOLARITY_FIELD: API_SCHOLARITY_FIELD,
    INPUT_FAMILYSTATUS_FIELD: API_FAMILYSTATUS_FIELD,
}

ADVANCE_TARGETING_FIELDS = [
    INPUT_INTEREST_FIELD, INPUT_BEHAVIOR_FIELD, INPUT_SCHOLARITY_FIELD, INPUT_FAMILYSTATUS_FIELD
]


# Old constants below ------------------------------------------------------------------------------------------
# MORE1M_USERS_COUNTRIES = ["AE","AF","AL","AO","AR","AT","AU","AZ","BA","BD","BE","BG","BO","BR","CA","CD","CH","CL","CM","CN","CO","CR","CZ","DE","DK","DO","DZ","EC","EG","ES","ET","FI","FR","GB","GE","GH","GR","GT","HK","HN","HR","HT","HU","ID","IE","IL","IN","IQ","IT","JM","JO","JP","KE","KH","KR","KW","KZ","LA","LB","LK","LT","LY","MA","MG","ML","MM","MN","MX","MY","MZ","NG","NI","NL","NO","NP","NZ","OM","PA","PE","PH","PK","PL","PT","PY","QA","RO","RS","RU","SA","SE","SG","SK","SN","SV","TH","TN","TR","TW","TZ","UA","UG","US","UY","VE","VN","YE","ZA","ZM"]
# MORE1M_USERS_COUNTRIES_old = ["IN","US","BR","ID","MX","PH","DE","GB","TR","FR","JP","IT","CA","ES","AU","AT","BE","CL","CZ","DK","FI","GR","HU","IE","IL","KR","NL","NZ","NO","PL","PT","SK","SE","CH"]
#
# # OECD Country List
# OECD_COUNTRIES = ["US","MX","DE", "GB", "TR", "FR","JP","IT","CA","ES","AU","AT","BE","CL","CZ","DK","EE","FI","GR","HU","IS","IE","IL","KR","LV","LU","NL","NZ","NO","PL","PT","SK","SI","SE","CH"]
# # English Spearker Countries
# COUNTRIES_ENGLISH = ["US","AU", "NZ", "IE", "IS", "GB", "CA", "PH", "IN"]
# # Western Europe Countries https://en.wikipedia.org/wiki/Western_Europe#Population
# EUROPE_WESTERN = ["AT","BE","DK","FI","FR","DE","GR","IS", "IE","IT","LU","NL","NO","PT","ES","SE","CH","GB"]
# # Too small facebook penetration countries
# SMALL_FB_COUNTRIES = ["CN","JP","IN","ID","KR"]
# NO_INTEREST_FLAG = "no_interest_selected"
#
#
# # Example of data_groups structure. Each item in "queries" correspond a one type of experiment that will be runned for  each country.
# # DATA_GROUPS = {
# #   "queries" :{
# #         [{
# #             "responses" : [],
# #             "requests"  : [],
# #             "csv_lines" : [],
# #         }],
# #     "correlation_lines" : []
# #     }
# # }
#
# GROUND_TRUTH_COLUMNS = [
#     "obesity",
#     "high_glucose",
#     "alcohol_dependeces",
#     "tobacco",
#     "war_disease",
#     "arab_interests",
#     "Pregnant Query Any Text 2"
# ]
# CSV_HEADERS = {
#     "data_header" : ["analysis_name","ground_truth_column","country_code","country_name","country_population","country_facebook_population","min_age","max_age","gender","interest","exclusion","placebo","audience","aud_fb_users","bid_amount_median","bid_amount_max","account_budget","pacing_status","dedup_status","bid_amount_min","estimate_DAU","unsupported","cpm_curve_data","cpc_curve_data","reach_max","dedup_winning_rate","reach_min","cpa_curve_data","location","estimate_ready","k=0.001","k=0.05","k=0.5","k=1","k=2","k=3","k=10","k=100","aud_placebo_aud","aud/pla_aud_k=0.001","aud/pla_aud_k=0.05","aud/pla_aud_k=0.5","aud/pla_aud_k=1","aud/pla_aud_k=2","aud/pla_aud_k=3","aud/pla_aud_k=10","aud/pla_aud_k=100","high_glucose","obesity","alcohol_dependeces","tobacco"],
#     "correlation_header" : ["interest","exclusion","k=0.001","k=0.05","k=0.5","k=1","k=2","k=3","k=10","k=100","aud/pla_aud_k=0.001","aud/pla_aud_k=0.05","aud/pla_aud_k=0.5","aud/pla_aud_k=1","aud/pla_aud_k=2","aud/pla_aud_k=3","aud/pla_aud_k=10","aud/pla_aud_k=100"]
# }
#
# placebo_index = 0