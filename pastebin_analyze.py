from pymongo import MongoClient
import argparse
from pprint import PrettyPrinter
import logging

pp = PrettyPrinter()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

logger = logging.getLogger(__name__)


def main():
    client = MongoClient(str(args['mongodbhost']), int(args['mongodbport']))
    db = client.scrape
    logger.info("MongoDB Connection created")

    dbcursor = db.pastebins.find({})

    # open keyword file
    file = open(args['f'], "r")
    search_exp = file.readlines()

    # per expression -> one collection in DB
    # Clear search_exp (whitespaces + \n)
    for exp in search_exp:
        clear_exp = exp.rstrip()

        # is the collection not already there?
        if clear_exp not in db.collection_names():
            db.create_collection(str(clear_exp))
            logger.info("MongoDB Collection new: " + str(clear_exp))

    # Iterate through documents
    for document in dbcursor:

        # Iterate through dictionary
        for key, value in document.items():

            # Iterate through keywords
            for exp in search_exp:
                clear_exp = exp.rstrip()

                if key == "title" or key == "user" or key == "content":

                    if value is not None:
                        splitted_string = value.split(' ')

                        # Compare every exp keyword with every other
                        # splitted string
                        for string in splitted_string:
                            if string == clear_exp:

                                # Check whether the pastebin has been added already
                                possible_pastebin = db[string].find_one({"key": document['key']})

                                if possible_pastebin is None:
                                    logger.info("Entry found for key: " + str(document['key']))

                                    # Insert Data into collection
                                    db[string].insert_one(document)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pastebin Analyzer - Offline")

    parser.add_argument('-f',
                        help="Config file containing all keywords to search for. Only matching pastebins will be saved.",
                        default="keywords.txt",
                        required=True)

    parser.add_argument('-mongodbhost',
                        help="A string with the URL to your MongoDB Server.",
                        default="localhost",
                        required=True)

    parser.add_argument('-mongodbport',
                        help="THe port to which your MongoDB listens.",
                        default=27017,
                        required=True)

    args = vars(parser.parse_args())

    main()