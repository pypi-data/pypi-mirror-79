#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creat dataset base on keywords

Usage:
  dataset_creator <env> <query>
  dataset_creator -h | --help

Options:
  -h --help         Show this screen.
  <query>           Text to search into begin image search engine
  <env>             Env file
"""

from __future__ import absolute_import

import logging.handlers
import os
import sys

import cv2
import requests
from docopt import docopt
from dotenv import load_dotenv
from requests import exceptions

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/dataset_creator.log",
                                                 when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

# Add the root folder to be able run this script and import utils package
sys.path.append(os.path.join(FOLDER_ABSOLUTE_PATH, '..'))


def get_number_of_files(folder_path):
    return len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])


def get(key, default=None):
    env_val = os.getenv(key, default)
    if env_val is None:
        raise Exception(f"The env name {key} need to be set into the .env file")
    return env_val


# construct the argument parser and parse the arguments
args = docopt(__doc__)

config = load_dotenv(args["<env>"])

# set your Microsoft Cognitive Services API key along with (1) the
# maximum number of results for a given search and (2) the group size
# for results (maximum of 50 per request)
API_KEY = get("API_KEY")
MAX_RESULTS = int(get("MAX_RESULTS", 250))
GROUP_SIZE = int(get("GROUP_SIZE", 50))

# set the endpoint API URL
URL = get("URL", "https://api.cognitive.microsoft.com/bing/v7.0/images/search")

OUTPUT_FOLDER = get("OUTPUT_FOLDER")

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# when attemping to download images from the web both the Python
# programming language and the requests library have a number of
# exceptions that can be thrown so let's build a list of them now
# so we can filter on them
EXCEPTIONS = {IOError, FileNotFoundError,
              exceptions.RequestException,
              exceptions.HTTPError,
              exceptions.ConnectionError,
              exceptions.Timeout}

# store the search term in a convenience variable then set the
# headers and search parameters
term = args["<query>"]
headers = {"Ocp-Apim-Subscription-Key": API_KEY}
params = {"q": term, "offset": 0, "count": GROUP_SIZE}

# make the search
PYTHON_LOGGER.info("searching Bing API for '{}'".format(term))
search = requests.get(URL, headers=headers, params=params)
search.raise_for_status()

# grab the results from the search, including the total number of
# estimated results returned by the Bing API
results = search.json()
estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
PYTHON_LOGGER.info("{} total results for '{}'".format(estNumResults, term))
# initialize the total number of images downloaded thus far
total = get_number_of_files(OUTPUT_FOLDER)
PYTHON_LOGGER.info("Number of images in this folder: {}".format(total))

# loop over the estimated number of results in `GROUP_SIZE` groups
for offset in range(0, estNumResults, GROUP_SIZE):
    # update the search parameters using the current offset, then
    # make the request to fetch the results
    PYTHON_LOGGER.info("making request for group {}-{} of {}...".format(
        offset, offset + GROUP_SIZE, estNumResults))
    params["offset"] = offset
    search = requests.get(URL, headers=headers, params=params)
    search.raise_for_status()
    results = search.json()
    PYTHON_LOGGER.info("saving images for group {}-{} of {}...".format(
        offset, offset + GROUP_SIZE, estNumResults))

    # loop over the results
    for v in results["value"]:
        # try to download the image
        try:
            # make a request to download the image
            PYTHON_LOGGER.info("fetching: {}".format(v["contentUrl"]))
            r = requests.get(v["contentUrl"], timeout=30)

            # build the path to the output image
            ext = v["contentUrl"][v["contentUrl"].rfind("."):]
            ext = ext.split('?')[0]
            p = os.path.sep.join([OUTPUT_FOLDER, "{}{}".format(str(total).zfill(8), ext)])

            # write the image to disk
            f = open(p, "wb")
            f.write(r.content)
            f.close()

        # catch any errors that would not unable us to download the
        # image
        except Exception as e:
            # check to see if our exception is in our list of
            # exceptions to check for:
            PYTHON_LOGGER.error("Error in the api query: {}".format(e))
            continue

        # try to load the image from disk
        image = cv2.imread(p)

        # if the image is `None` then we could not properly load the
        # image from disk (so it should be ignored)
        if image is None:
            PYTHON_LOGGER.info("deleting: {}".format(p))
            os.remove(p)
            continue

        # update the counter
        total += 1
