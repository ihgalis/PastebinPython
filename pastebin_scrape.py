from pastebin_python.pastebin import PastebinPython
from pastebin_python.pastebin_exceptions import PastebinBadRequestException
from pymongo import MongoClient
from copy import deepcopy

import json
import urllib.request
import argparse
import logging
import time

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

logger = logging.getLogger(__name__)


def call_scrape_url(url):
    """
    Method is doing all the URL calling stuff.

    :param url: The URL which should be called
    :return: The content of the previously requested pastebin
    """

    try:
        request = urllib.request.Request(url)
        result = urllib.request.urlopen(request)
        result_text = result.read()
        text_encoded = result_text.decode(encoding='utf-8', errors='ignore')

        return text_encoded

    except json.decoder.JSONDecodeError as json_e:
        logger.error("JSON Decoding Error ... Jumping to next element.")
        return None


def main(args):
    """
    Regular main method starts the entire process and interprets the
    arguments.

    :param args: arguments from argparse
    :return: None
    """

    if args['v'] == 0:
        logger.propagate = False
    elif args['v'] == 1:
        logger.propagate = True

    logger.info("Start Pastebin Analyzer")

    api_key = args['api']
    pbin = PastebinPython(api_dev_key=api_key)

    client = MongoClient(str(args['mongodbhost']), int(args['mongodbport']))
    db = client.scrape
    logger.info("MongoDB Connection created")

    while True:
        try:
            data = pbin.scrapeMostRecent()

            if data:
                json_data = data.decode('utf8')  # .replace("'", '"')
                final_data = json.loads(json_data)

                # Iterate through list
                for x in final_data:

                    # Pre-create the content key-value pair
                    x['content'] = 0

                    copy_of_x = deepcopy(x)
                    for key, value in copy_of_x.items():

                        if key == "scrape_url":

                            # value = scrape_url
                            text_encoded = call_scrape_url(value)
                            time.sleep(1)

                            logger.info("Downloading content of " + value)

                            # Add content
                            x['content'] = text_encoded

                            ## TODO: Add some identity check

                            # DB Save mode args['db'] == 2
                            if args['db'] == "1":
                                db.pastebins.insert_one(x)
            else:
                logger.debug("No data arrived.")

        except PastebinBadRequestException as e:
            logger.debug("Pastebin Bad Request - You're doing it wrong")

        except json.decoder.JSONDecodeError as e:
            logger.debug("JSON Decoding Error ... 'You can't always get what you want!'")
            continue
        else:
            logger.debug("No exception")
        finally:
            logger.info("End of Session!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pastebin Analyzer")

    parser.add_argument('-db',
                        help="If this is set entries are being added into the DB.\n"
                             "0 = no DB entries"
                             "1 = all Pastebin entries are written to DB",
                        default=0)

    parser.add_argument('-v',
                        help="Verbose mode.",
                        default=0)

    parser.add_argument('-api',
                        help="Pastebin API Key for Scraping.",
                        required=True)

    parser.add_argument('-mongodbhost',
                        help="A string with the URL to your MongoDB Server.")

    parser.add_argument('-mongodbport',
                        help="THe port to which your MongoDB listens.",
                        default=27017)

    args = vars(parser.parse_args())

    main(args)
