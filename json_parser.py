# -*- coding: utf-8 -*-
"""json_parser Module.

This module is created to parse both phishing and legit web-pages and add them to MongoDB.


"""

import json

from pymongo import MongoClient


def to_mongodb(domain):
    """ Funtion add domain to MongoDB

    Args:
        domain: (str) Domain name

    """
    db_client = MongoClient()
    db = db_client.phishing
    db.whitelist.insert_one(
        {
            "legitimate": {
                "domain_name": domain
            }
        }
    )


def phsihing_to_db():
    """Get scrapped phishtank Json file, parses JSON
    and adds links to MongoDB

    """
    jsonFile = open('phishtank/links.json', 'r')
    data = json.load(jsonFile)
    jsonFile.close()

    link_array = []

    for index in data:
        link_array.append(index['url'])

    print (len(link_array))

    for link in link_array:
        to_mongodb(link)


def legit_to_db():
    """Get Legit pages from scrapper and adds it to MongoDB

    """
    text_file = open("alexa/legit.txt", "r")
    lines = text_file.read().split('\n')

    for line in lines:
        domain = line.replace(" ", "")
        to_mongodb(domain)
