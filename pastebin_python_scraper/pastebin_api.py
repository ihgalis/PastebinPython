from flask import Flask, jsonify, make_response
from pymongo import MongoClient
from bson import json_util

import argparse
import json

app = Flask(__name__)

api_version = "1.0"


@app.errorhandler(404)
def not_found(error):
    """
    some standard error handling for unknown pages.

    :param error:
    :return:
    """
    return make_response(jsonify({'error': 'Notfound'}), 404)


@app.route('/')
def get_index():
    """
    standard output when nothing is set
    :return:
    """

    basic_info = [
        {
            'api': '1.0',
            'name': 'PastebinPython Flask Accessing API',
            'author': 'Andre Fritsche / ihgalis'
        }
    ]

    return jsonify({'basic_info': basic_info})


@app.route('/api/getpastebins/<string:keyword>', methods=['GET'])
def get_pastebins(keyword):
    """
    method gets all documents related to the specified keyword. It accesses the corresponding collections so you will
    always get only the documents that have been identified by the pastebin_analyze.py script.

    :param keyword: string
    :return: JSON based dictionary
    """

    client = MongoClient(str(args['mongodbhost']), int(args['mongodbport']))
    db = client.scrape

    tlist = list()

    dbcursor = db[keyword].find({})
    for document in dbcursor:
        sanitized = json.loads(json_util.dumps(document))
        tlist.append(sanitized)

    return jsonify(tlist)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PastebinPython Flask Accessing API")

    parser.add_argument('-mongodbhost',
                        help="A string with the URL to your MongoDB Server.",
                        default="localhost",
                        required=True)

    parser.add_argument('-mongodbport',
                        help="THe port to which your MongoDB listens.",
                        default=27017,
                        required=True)

    parser.add_argument('-d',
                        action="store_true",
                        help="Debug in Flask active or not.",
                        default=0)

    args = vars(parser.parse_args())

    if args['d']:
        app.run(debug=True)
    else:
        app.run(debug=False)
