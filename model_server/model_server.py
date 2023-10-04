# (c) 2015 - 2023 Open Risk (https://www.openriskmanagement.com)
"""
@author: open risk
Purpose: Demonstration of Open Risk Model API compliant model server
Version: 0.1

Implements model service point
- accepts a json formated calculation script via POST
- connects to data point(s) and gets required data
- performs calculations
"""

import json

import numpy as np
import requests
from bson.objectid import ObjectId
from flask import Flask, request
from pymongo import MongoClient
from rdflib import Literal, Graph, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF

import concentration_library as cl

PORT = 5012
ENTRY_POINT = "http://127.0.0.1:" + str(PORT)
DEBUG = True

app = Flask(__name__)


def get_data(portfolio_url):
    r = requests.get(portfolio_url)
    return r.json()


# the model collection
def calculate(model_name, portfolio_url):
    print(model_name)
    # Exctract exposure data for calculation
    portfolio_raw = get_data(portfolio_url)
    portfolio_list = []
    for entry in portfolio_raw['_items']:
        portfolio_list.append(entry['EAD'])
    portfolio = np.array(portfolio_list)
    weights = cl.get_weights(portfolio)
    if model_name == 'shannon':
        value = cl.shannon(weights)
    elif model_name == 'hhi':
        value = cl.hhi(weights)
    return {"result": value}


@app.route('/', methods=['GET'])
@app.route('/models', methods=['GET'])
def return_models_list():
    # currently we have an in memory description of the models list
    # in production this will be a dynamically updated rdf/jsonld triplestore

    ns = Namespace("http://openriskplatform.org/ns/doam#")

    # create an RDF graph with model data
    g = Graph()
    # identify models via their URI
    hhi = URIRef(ENTRY_POINT + "/models/hhi")
    # add model metadata
    g.add((hhi, RDF.type, ns['model']))
    g.add((hhi, FOAF.nick, Literal("hhi", lang="en")))
    g.add((hhi, FOAF.name, Literal("Hirschman")))
    g.add((hhi, ns['name'], Literal("HHI")))

    shannon = URIRef(ENTRY_POINT + "/models/shannon")
    g.add((shannon, RDF.type, ns['model']))
    g.add((shannon, FOAF.nick, Literal("sha", lang="en")))
    g.add((shannon, FOAF.name, Literal("Shannon")))
    g.add((shannon, ns['name'], Literal("Shannon")))

    # DEBUG STEP Iterate over triples in store and print them out
    if DEBUG:
        print("--- printing raw triples ---")
        for s, p, o in g:
            print((s, p, o))

    # Now that we have all general model information create json-ld output
    # Bind a few prefix, namespace pairs for more readable output
    g.bind("dc", DC)
    g.bind("foaf", FOAF)
    model_list = g.serialize(format="json-ld")
    return model_list


@app.route('/models/<model_name>', methods=['GET'])
def return_model_description(model_name):
    # return an in memory description of model

    ns = Namespace("http://openriskplatform.org/ns/doam#")
    # print(model_name)

    # identify model via its URI
    if model_name == 'hhi':
        model = URIRef(ENTRY_POINT + "/models/" + 'hhi')
    elif model_name == 'shannon':
        model = URIRef(ENTRY_POINT + "/models/" + 'shannon')
    else:
        print("Invalid model name")

    # identify portfolio server via its URI
    portfolio = URIRef("http://127.0.0.1:5011/obligors/")
    # identify output storage via its URI (foobar)
    results = URIRef("http://127.0.0.1:5010/results/")

    g = Graph()
    # Add triples using store's add method.
    g.add((model, RDF.type, ns['model']))
    g.add((model, FOAF.name, Literal(model_name)))
    g.add((model, FOAF.mbox, URIRef("mailto:models_r_us@example.org")))
    g.add((model, ns['name'], Literal(model_name)))
    g.add((model, ns['hasInput'], portfolio))
    g.add((model, ns['hasOutput'], results))

    # DEBUG STEP Iterate over triples in store and print them out
    if DEBUG:
        # Iterate over triples in store and print them out.
        print("--- printing raw triples ---")
        for s, p, o in g:
            print((s, p, o))

    # Now that we have all the specific model information create json-ld output
    # Bind a few prefix, namespace pairs for more readable output
    g.bind("dc", DC)
    g.bind("foaf", FOAF)
    model_description = g.serialize(format="json-ld")
    return model_description


@app.route('/models/<model_name>', methods=['POST'])
def calculation(model_name):
    # build input ticket
    calculation_input = request.json
    # to add request timestamp
    # connection to local storage (MongoDB instance)
    client = MongoClient('mongodb://localhost:27017/')
    # select calculations database
    db = client.calculations
    # select inputs collection
    inputs_list = db.inputs
    # convert ticket into json (double quote workaround)
    t1 = json.dumps(calculation_input)
    t2 = json.loads(t1)
    # insert ticket into storage (portfolio.inputs)
    # for future use, currently not accessible from the API
    input_id = inputs_list.insert(t2)

    # perform the calculation
    # store the result in local storage
    # return an output URL
    portfolio_url = calculation_input["portfolio_url"]
    result = calculate(model_name, portfolio_url)
    # print(result)
    # result = {"result" : 0}
    # select outputs collection
    outputs_list = db.outputs
    t1 = json.dumps(result)
    t2 = json.loads(t1)
    output_id = outputs_list.insert(t2)

    # build output response (use input data + calculation URI etc)
    calculation_output = {}
    calculation_output["user_id"] = calculation_input["user_id"]
    calculation_output["output_url"] = calculation_input["model_url"] + "/" \
                                       + str(output_id)
    return json.dumps(calculation_output)


@app.route('/models/<model_name>/<calc_id>', methods=['GET'])
def display_results(model_name, calc_id):
    # print(model_name, calc_id)
    # connection to local storage (MongoDB instance)
    client = MongoClient('mongodb://localhost:27017/')
    # select calculations database
    db = client.calculations
    # select outputs collection
    outputs_list = db.outputs
    # find result by its ID
    # calc_id = '"' + calc_id + '"'
    object_id = {"_id": ObjectId(calc_id)}
    # print(object_id)
    cursor = outputs_list.find(object_id)
    for doc in cursor:
        result = doc["result"]
    return json.dumps(result)


if __name__ == '__main__':
    app.run(port=PORT, debug=True)
