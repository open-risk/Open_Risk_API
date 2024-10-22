# encoding: utf-8

# (c) 2017-2021 Open Risk, all rights reserved
#
# Concentration Library is licensed under the MIT license a copy of which is included
# in the source distribution of TransitionMatrix. This is notwithstanding any licenses of
# third-party software included in this distribution. You may not use this file except in
# compliance with the License.
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.

"""
Created on Fri Nov 18 14:24:07 CET 2017
@author: Open Risk
Purpose: Implement flask based Open Risk API Model Server
Version: 0.2

Model_Server.py implements the basic Semantic REST API
- dependencies are http / semantic libs
- handles json data format

"""

import os
import json
# import requests
from rdflib import Literal, Graph, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF

from Compute import calculate

# You can insert another directory for model code here
# SOURCE_DIR = '/path/to/the/source/code/here'
SOURCE_DIR = os.path.dirname(__file__) + '/'

from flask import Flask, request

app = Flask(__name__)

DEBUG = False


@app.route('/', methods=['GET'])
def return_api_basics():
    api_basics = {
        '/model_list/': ['GET'],
        '/&ltmodel_name&gt': ['GET', 'POST'],
        '/&ltmodel_name&gt/workflows': ['GET']
    }
    return json.dumps(api_basics)


@app.route('/model_list/', methods=['GET'])
def return_model_list():

    # currently we load an in memory description of the model list from a rdf file
    # in production this will be a dynamically updated rdf/jsonld triplestore

    ns = Namespace("http://www.openriskplatform.org/ns/doam#")

    # create an RDF graph with model data
    g = Graph()
    # result = g.parse('/var/www/model_server/model_list.rdf')
    result = g.parse(SOURCE_DIR + 'model_list.rdf')

    # DEBUG STEP Iterate over triples in store and print them out
    if DEBUG:
        print("=== printing model list raw triples ===")
        for s, p, o in g:
            print((s, p, o))

    # Now that we have all general model information create json-ld output
    model_list = g.serialize(format="json-ld")
    return model_list


@app.route('/<model_name>', methods=['GET'])
def return_model_description(model_name):
    # return an in memory description of model
    # print(model_name)

    not_found_string = 'Model file not found'
    could_not_parse_string = 'Model file could not be parsed'

    rdf_file = SOURCE_DIR + model_name + '.rdf'

    context = {"doam": "http://www.openriskplatform.org/ns/doam#",
                "owl": "http://www.w3.org/2002/07/owl#",
                "XMLSchema": "http://www.w3.org/2001/XMLSchema#"}

    if os.path.isfile(rdf_file):
        try:
            g = Graph()
            result = g.parse(rdf_file)

            # DEBUG STEP Iterate over triples in store and print them out
            if DEBUG:
                # Iterate over triples in store and print them out.
                print("--- printing model info raw triples ---")
                for s, p, o in g:
                    print((s, p, o))

                    # Now that we have all the specific model information create json-ld output
                    # Bind a few prefix, namespace pairs for more readable output
            model_description = g.serialize(format="json-ld")
            return model_description

        except:
            return json.dumps({"Error": could_not_parse_string})

    else:
        return json.dumps({"Error": not_found_string})


@app.route('/<model_name>', methods=['POST'])
def calculation_request(model_name):

    # This version implements a simplified version of the Open Risk Workflow API
    # No model parameters
    # No permanent storage

    data = request.json
    output = calculate(model_name, data)
    result = json.dumps(output)
    return result


if __name__ == '__main__':
    app.run(debug=True)
