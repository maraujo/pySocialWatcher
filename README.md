# pySocialWatcher
### A Social Data Collector from Facebook Marketing API
#### I'm more than pleased that many teams used this library. But I need your help to support it. Please feel free to pull requests that solve issues. Unfortunatelly, my time is very very limited to keep updating this repository.
#### If this package helps your research somehow, reference this paper:

```
@inproceedings{araujo2017facebook,
 author = {Araujo, Matheus and Mejova, Yelena and Weber, Ingmar and Benevenuto, Fabricio},
 title = {Using Facebook Ads Audiences for Global Lifestyle Disease Surveillance: Promises and Limitations},
 series = {WebSci '17},
 year = {2017},
 location = {Troy, USA},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {Facebook, Advertising, Epidemihology, Social Media, Health},
} 
```

 
[![Build Status](https://travis-ci.org/maraujo/pySocialWatcher.svg?branch=master)](https://travis-ci.org/maraujo/pySocialWatcher)
[![codecov](https://codecov.io/gh/maraujo/pySocialWatcher/branch/dev/graph/badge.svg)](https://codecov.io/gh/maraujo/pySocialWatcher)

**Package Name:** pysocialwatcher

**Facebook Ads API version supported:** 2.9

**License:** MIT

**Python Version:** 2.7


### What is this for
This package tries to get the full potencial of the Facebook Marketing API for Social Analysis research.
Recent works show that online social media has a huge potencial to provide interesting insights on trends of across demographic groups.

Examples of research question that it can answer:
* For each european country, get how many people are interested in Science?
* Get how many people in each GCC country who is Graduated AND is interested in Football, and how many is not interested in Football breakdown by: gender, age range, scholarity, language and citizenship.


##### Facebook Marketing API Refereces page:
Targeting Specs: https://developers.facebook.com/docs/marketing-api/targeting-specs/v2.8

Ad Targeting Search API: https://developers.facebook.com/docs/marketing-api/targeting-search/v2.8
### Limitations:
* Current supported API fields are listed below:
    ```
    "interests",
    "behaviors",
    "education_statuses",
    "family_statuses",
    "relationship_statuses",
    "locales",
    "genders",
    "age_min",
    "age_max",
    "geo_locations"
    ```

### Install
    git clone https://github.com/maraujo/pySocialWatcher.git
    cd pySocialWatcher
    pip install -r requirements.txt
    python setup.py install
    
### Quick Start
You should have a .csv file with your Facebook tokens and accountIDs.
Example: pySocialWatcher/pysocialwatcher/facebook_tokens_example.csv
  
    >>> from pysocialwatcher import watcherAPI 
    >>> watcher = watcherAPI() 
    >>> watcher.load_credentials_file("pysocialwatcher/credentials.csv")
    >>> watcher.run_data_collection("pysocialwatcher/input_examples/quick_example.json")

### How it works (slides):
Check the slides: https://goo.gl/WzE9ic

### Features
1. Static input json format to make you experiments easily reproducible.
2. Support multiple Facebook tokens.
3. Multiple tokens are processed in parallel to speedup data collection.
3. Complex logic queries in the Facebook Marketing API with 'or', 'and', 'not', for example:.
```
      "interests": [{
            "not": [6003442346642],
            "and": [6004115167424, 6003277229371],
            "name": "Not interested in Football, but interest in some physical activity"
        }
```
4. Automatically save the state every constants.SAVE_EVERY requests. If any problem happens you can load the incomplete file and continue the data collection (```load_data_and_continue_collection```)

#### Input Json Format Example

The following input is an example of input format of the package. In this example it will perform several requests in the Facebook Marketing API in order to collect the audience realted to Soccer Interest in GCC countries.

    {   "name": "Soccer Interest",
         "geo_locations": [
              { "name": "countries", "values": ["BH"] },
              { "name": "countries", "values": ["KW"] },
              { "name": "countries", "values": ["OM"] },
              { "name": "countries", "values": ["QA"] },
              { "name": "countries", "values": ["SA"] },
              { "name": "countries", "values": ["AE"] }
    ],
    "genders": [1,2],
    "ages_ranges": [
        {"min":18, "max":24},
        {"min":55}
    ],
    "scholarities":[{
        "name" : "Graduated",
        "or" : [3,7,8,9,11]
      }
    ],
    "languages":[{
        "name" : "Arabic",
        "values" : [28]
        },
        null
    ],
    "behavior": [
        {
          "or": [6015559470583],
          "name": "Expats"
        },
        {
          "not": [6015559470583],
          "name": "Not Expats"
        }
    ],
    "interests": [{
            "not": [6003442346642],
            "and": [6004115167424, 6003277229371],
            "name": "Not interested in Football, but interest in physical activity"
        },{
            "or": [6003442346642],
            "name" : "Football"
        }
    ]
    }
In total it will perform 192 requests which are created in the following way:
```
For each GCC country in the geo_locations field:
    For each gender in [1,2]:
        For each age range in [18-24,55+]:
            For each scholarity group:
                For each language group:
                    For each behavior group:
                        For each interest group:
                            doFacebookAPIRequest()
            
```
So it will collect the audience for all of the combinations specified in the input file. If you don't want to specify a specific field you can ommit in the input or put a null value in the list like:
```
"languages":[{
    "name" : "Arabic",
    "values" : [28]
    },
    null
],

```
#### Find Targeting IDs given Query
    >>> from pysocialwatcher import watcherAPI 
    >>> watcher = watcherAPI() 
    >>> watcher.load_credentials_file("pysocialwatcher/credentials.csv")
    >>> watcher.print_search_targeting_from_query_dataframe("Parents")
    
    +----+-----------------+----------------------------------------+------------------+------------------------------------------------------+---------------------------------------------------------------------------------------------------------+-------------------+
    |    |   audience_size | description                            |               id | name                                                 | path                                                                                                    | type              |
    |----+-----------------+----------------------------------------+------------------+------------------------------------------------------+---------------------------------------------------------------------------------------------------------+-------------------|
    |  0 |       286670228 | People who are parents.                |    6002714398372 | Parents (All)                                        | [u'Demographics', u'Parents', u'All Parents', u'Parents (All)']                                         | family_statuses   |
    |  1 |        92661179 | Parents with children 18-26 years old. |    6023005718983 | (18-26 Years) Parents with Adult Children            | [u'Demographics', u'Parents', u'All Parents', u'(18-26 Years) Parents with Adult Children ']            | family_statuses   |
    |  2 |        45169601 | Parents with children 13-18 years old. |    6023005681983 | (13-18 Years) Parents with Teenagers                 | [u'Demographics', u'Parents', u'All Parents', u'(13-18 Years) Parents with Teenagers ']                 | family_statuses   |
    |  3 |        13123437 | Parents with Children ages 8-12        |    6023080302983 | (08-12 Years) Parents with Preteens                  | [u'Demographics', u'Parents', u'All Parents', u'(08-12 Years) Parents with Preteens']
    ...
    
#### Find Interest IDs given name Name
    >>> from pysocialwatcher import watcherAPI 
    >>> watcher = watcherAPI() 
    >>> watcher.load_credentials_file("pysocialwatcher/credentials.csv")
    >>> watcher.print_interests_given_query("Family")
    
    +----+------------+---------------+--------------------------+--------------------------------------------------------------------+
    |    |   audience |   interest_id | name                     | path                                                               |
    |----+------------+---------------+--------------------------+--------------------------------------------------------------------|
    |  0 | 1019524230 | 6012684376438 | Family and relationships | [u'Interests', u'Family and relationships']                        |
    |  1 |  788072890 | 6003476182657 | Family                   | [u'Interests', u'Family and relationships', u'Family']             |
    |  2 |  178716020 | 6003190413105 | Family (biology)         | [u'Interests', u'Additional Interests', u'Family (biology)']       |
    |  3 |   58127760 | 6003206382686 | family  planning         | [u'Interests', u'Additional Interests', u'family  planning']       |
    |  4 |   25284610 | 6002966041646 | family films             | [u'Interests', u'Additional Interests', u'family films']           |
    |  5 |   18734150 | 6003305411169 | Family Guy               | [u'Interests', u'Additional Interests', u'Family Guy']             |
    |  6 |   12447740 | 6003455599405 | Royal family             | [u'Interests', u'Additional Interests', u'Royal family']           |
    |  7 |   10252970 | 6003143952966 | Family of Barack Obama   | [u'Interests', u'Additional Interests', u'Family of Barack Obama'] |
    +----+------------+---------------+--------------------------+--------------------------------------------------------------------+

#### Find Behavior IDs Lists
    >>> from pysocialwatcher import watcherAPI 
    >>> watcher = watcherAPI() 
    >>> watcher.load_credentials_file("pysocialwatcher/credentials.csv")
    >>> watcher.print_behaviors_list()
    +-----+------------+---------------+-------------------------------------------------------------------------------------------------------------------+----------------------------------------------------+--------------------------------------------------------------------------------------------+
    |     |   audience |   behavior_id | description                                                                                                       | name                                               | path                                                                                       |
    |-----+------------+---------------+-------------------------------------------------------------------------------------------------------------------+----------------------------------------------------+--------------------------------------------------------------------------------------------|
    |   0 |  249325232 | 6002714895372 | People whose activities on Facebook suggest they are Frequent travelers.                                          | All frequent travelers                             | [u'Travel', u'All frequent travelers']                                                     |
    |   1 |   34932108 | 6002714898572 | People who list themselves as small business owners or own small business pages on Facebook                       | Small business owners                              | [u'Digital activities', u'Small business owners']                                          |
    |   2 |    6444115 | 6002764392172 | People who have used Facebook Payments platform in the past 90 days                                               | FB Payments (All)                                  | [u'Digital activities', u'FB Payments (All)']                                              |
    |   3 |   91484312 | 6003050295572 | Users who uploaded >50 photos on Facebook in last month.                                                          | Photo uploaders
    ...

#### Find Geo Location Key Given Query and Location Type
    >>> from pysocialwatcher import watcherAPI 
    >>> watcher = watcherAPI() 
    >>> watcher.load_credentials_file("pysocialwatcher/credentials.csv")
    >>> watcherAPI.print_geo_locations_given_query_and_location_type("new", ["city"])
    +----+---------+-------------------------+-----------------+-------------------+--------+
    |    |     key | name                    |   supports_city |   supports_region | type   |
    |----+---------+-------------------------+-----------------+-------------------+--------|
    |  0 | 2490299 | New York                |               1 |                 1 | city   |
    |  1 | 2490287 | New Rochelle            |               1 |                 1 | city   |
    |  2 | 2528778 | New Braunfels           |               1 |                 1 | city   |
    |  3 | 2511352 | New Castle              |               1 |                 1 | city   |
    ....

#### Find all Geo Locations Given Location Type and Country
    >>> from pysocialwatcher import watcherAPI 
    >>> watcher = watcherAPI() 
    >>> watcher.load_credentials_file("pysocialwatcher/credentials.csv")
    >>> watcherAPI.print_geo_locations_given_query_and_location_type(None, ["region"], country_code='ID')

    +----+----------------+----------------+-------+------------------------------+-----------------+-------------------+--------+
    |    | country_code   | country_name   |   key | name                         | supports_city   | supports_region   | type   |
    |----+----------------+----------------+-------+------------------------------+-----------------+-------------------+--------|
    |  0 | ID             | Indonesia      |  1662 | Bali                         | True            | True              | region |
    |  1 | ID             | Indonesia      |  1676 | East Nusa Tenggara           | True            | True              | region |
    |  2 | ID             | Indonesia      |  1685 | West Java                    | True            | True              | region |
    |  3 | ID             | Indonesia      |  1675 | West Nusa Tenggara           | True            | True              | region |
    ...
    
#### Find KML Given Location Key and Location Type
    >>> from pysocialwatcher import watcherAPI 
    >>> watcher = watcherAPI() 
    >>> watcher.load_credentials_file("pysocialwatcher/credentials.csv")
    >>> watcherAPI.get_kml_given_geolocation("countries", ["BR","CL","AT","US","QA"])
    +----+---------------------------------------------------+-------------------+
    |    |     kml                                           | name              |
    |----+---------------------------------------------------+-------------------+
    |  0 | <Polygon><outerBoundaryIs><LinearRing><coordin... | Brazil            |
    |  1 | <Polygon><outerBoundaryIs><LinearRing><coordin... | Chile             |
    |  2 | <Polygon><outerBoundaryIs><LinearRing><coordin... | Austria           |
    |  3 | <Polygon><outerBoundaryIs><LinearRing><coordin... | United States     |
    ....


#### Advaced Configurations
##### Change Sleep time between requests to 10s:

    from pysocialwatcher import constants
    constants.SLEEP_TIME = 10

##### Change save temporary file every 1000 requests:

    from pysocialwatcher import constants
    constants.SAVE_EVERY = 1000
  
##### Specify that results should be saved to the directory `data/pySocialWatcher/test_query_results/`

    watcher.run_data_collection("pySocialWatcher/pysocialwatcher/quick_example.json", 
                                "data/pySocialWatcher/test_query_results/")

_Note: Assumes that the directory already exists. Filepath is added to the beginning of the output `.csv` files generated._ 


### Potential Issues:
1. If you received the error: *You are calling a deprecated version of the Ads API*, means that Facebook updated the API. One way to fix is changing the first 3 variables of the constants.py file to the current Facebook API. This does not guarantee that everything will work.

### Change Log
* 2.0a - Fix bug from @joaopalotti and thank @KangboLu, @kpolimis, @khof312 for previous commits.
* 0.1j - Get more informative dataframes from: get_behavior_dataframe, get_interests_given_query, get_search_targeting_from_query_dataframe
* 0.1i - Errors more understable and some small fixes.
* 0.1h - AND working for behavior. Thanks @ianbstewart.
* 0.1g - Besides MAU, now we also captures DAU. Thanks @VatsalaSingh.
* 0.1f - Call version v2.11 of Facebook Marketing API
* 0.1e - Add support to *not* for demographics that uses specific integer numbers such as scholarity
* 0.1d - Add support to household_composition
* 0.1b2 - Add support to relationship_statuses and check input keys
* 0.1b0 - Search any query with get_search_targeting_from_query_dataframe()
* 0.1a3 - Resilient error handling when error code = 2 (try again more constants.MAX_NUMBER_TRY times)
* 0.1a2 - Fix bug when have multiple operators like (and, not) in the same query
* 0.1a1 - Add MIT License and 'Geo Location' field support in facebook API
* 0.1a0 - First Alpha Release
