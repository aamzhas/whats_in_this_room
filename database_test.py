#!/usr/bin/env python

"""

"""

import pymongo

import mongo_credentials

__author__ = "Aamir Hasan"
__version__ = "1.0"
__email__ = "hasanaamir215@gmail.com"

client = pymongo.MongoClient("mongodb://" + mongo_credentials.username + ":"
                             + mongo_credentials.password + "@ds141812.mlab.com:41812/uiuc_classrooms")
database = client['uiuc_classrooms']
collection = database['data']

query = {"room_number": 215, "building_name": "Gregory Hall", "start_time": "11:00 AM"}

doc = collection.find(query)

for x in doc:
    print(x['course_name'])
