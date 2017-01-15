# pySocialWatcher
###A Social Data Collector from Facebook Marketing API
 
[![Build Status](https://travis-ci.org/maraujo/pySocialWatcher.svg?branch=dev)](https://travis-ci.org/maraujo/pySocialWatcher)
[![codecov](https://codecov.io/gh/maraujo/pySocialWatcher/branch/dev/graph/badge.svg)](https://codecov.io/gh/maraujo/pySocialWatcher)
**Package Name:** pySocialWatcher

**Facebook Ads API version supported:** 2.8


### What is this for
This application tries to get the full potencial of the Facebook Marketing API for Social Analysis research.
Recent works show that online social media has a huge potencial to provide interesting insights on trends of across demographic groups.

### Install
    pip install -r requirements.txt
    python setup install
    
### Quick Start
You should have a .csv file with your Facebook tokens and accountIDs.
Example: pySocialWatcher/pysocialwatcher/facebook_tokens_example.csv
  
    >>> from pysocialwatcher import watcherAPI 
    >>> watcher = watcherAPI() 
    >>> watcher.load_credentials_file("pysocialwatcher/credentials.csv")
    >>> watcher.run_data_collection("pySocialWatcher/pysocialwatcher/quick_example.json")

### Features
1. Static input json format to make you experiments easily reproducible.
2. Support multiple Facebook tokens.
3. Tokens are processed in parallel to speedup data collection.
3. Comples logic queries in the Facebook Marketing API with 'or', 'and', 'not', check the input_examples.
4. Current supported fields:
    ```
    "interests"
    "behaviors"
    "education_statuses"
    "family_statuses"
    "locales"
    "genders"
    "age_min"
    "age_max"
    ```

#### Input Json Format Example
    {
        "name": "Luxury in Bahrein and Argelia",
        "location": ["DZ","BH"],
        "genders": [0],
        "ages_ranges": [
            {"min":18, "max":24}
        ],
        "scholarities":[{
            "name" : "Graduated",
            "or" : [3,7,8,9,11]
        }],
        "languages":[{
            "name" : "Arabic",
            "or" : [28]
         }],
        "behavior": [
            {
            "or": [6015559470583],
            "name": "Expats"
         }],
        "interests": [{
            "or": [6007828099136,6003392552125,6002991798459,6003132627317,6003488503154,6004048615096,6003840055852,6003103779434,6003401661947,6003167425934,6003263791114,6003346592981,6003390752144,6003325662688,6004037400009,6003372667195,6003089951815,6003398056603,6002971085794,6003289911338,6003188427578,6002944044446,6003509853804],
            "name": "luxury"
        }]
    }

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

#### Advaced Configurations
#####Change Sleep time between requests to 10s:

    from pysocialwatcher import constants
    constants.SLEEP = 10

#####Change save temporary file every 1000 requests:

    from pysocialwatcher import constants
    constants.SAVE_EVERY = 1000


### Change Log
* 0.1a0 - First Alpha Release