# (c) 2015 - 2023 Open Risk (https://www.openriskmanagement.com)

"""
@author: open risk
Purpose: Demonstration of Open Risk Model API client queries
Version: 0.1

This client emulates a typical user path exploring the API
"""

import requests
import json

from rdflib import Graph, Namespace, RDF

# The entry point for the model server (assumed known)
# location of registry (same as model server for now)
PORT = 5012
ENTRY_POINT = "http://127.0.0.1:" + str(PORT)


def get_data_dictionaries():

    # TODO get dictionaries for data fields
    return


def get_models_list(model_server_url):
    # get all model information from a model registry
    # location of ontology (rdf/xml)
    # ns = Namespace("http://openriskplatform.org/ns/doam#")
    # entry point for model registry is assumed known
    # get a model list (format is json-ld)
    model_list = requests.get(model_server_url)
    response = model_list.json()

    # print("--- print json-ld response ---")
    # print(model_list.text)

    # parse json-ld into graph
    rdf1 = json.dumps(response)
    g = Graph()
    g.parse(data=rdf1, format="json-ld")
    return g


def print_models_list(graph):
    ns = Namespace("http://openriskplatform.org/ns/doam#")
    # For each doam:Model in the store print out its name property.
    for model in graph.subjects(RDF.type, ns['model']):
        for name in graph.objects(model, ns['name']):
            print(name.toPython(), model.toPython())
    return


def get_model_info(g, model_name):
    # select and query a model server on the basis of model name
    for model in g.subjects(RDF.type, ns['model']):
        for name in g.objects(model, ns['name']):
            if name.toPython() == model_name:
                model_url = model.toPython()

    model_info = requests.get(model_url)
    # print("--- print json-ld response ---")
    # print(model_info.text)

    response2 = model_info.json()
    rdf2 = json.dumps(response2)
    g2 = Graph()
    g2.parse(data=rdf2, format="json-ld")
    return g2


def print_model_info(graph):
    for s, p, o in graph:
        print(s.toPython(), p.toPython(), o.toPython())


def get_data(portfolio_url, query):
    r = requests.get(portfolio_url + query)
    return r.json()


def post_calculation_ticket(model_url, ticket):
    headers = {'Content-Type': 'application/json'}
    print(json.dumps(ticket))
    response = requests.post(model_url, data=json.dumps(ticket), headers=headers)
    print(response.json())
    return response


def get_results(results_url):
    r = requests.get(results_url)
    return r.json()


if __name__ == '__main__':

    # Required to resolve semantics, assumed known
    ns = Namespace("http://openriskplatform.org/ns/doam#")

    # ACTION 1
    # initialize exploration of API
    print("--- Action 1: print model names and URL's ---")
    model_list = get_models_list(ENTRY_POINT + '/models')
    print_models_list(model_list)

    # ACTION 2
    # get specific model info by name (provided by previous step)
    # Choice 1: HHI
    # Choice 2: Shannon
    print("--- Action 2: print the data of a selected model ---")
    model_name = 'Shannon'
    model_info = get_model_info(model_list, model_name)
    print_model_info(model_info)

    # Extract information from graph for more convenient use by the client
    # The hasOutput field can be used to redirect output to a different server
    # Not used at present
    for model in model_info.subjects(RDF.type, ns['model']):
        model_url = model.toPython()
        for data in model_info.objects(model, ns['hasInput']):
            portfolio_url = data.toPython()
        for data in model_info.objects(model, ns['hasOutput']):
            output_url = data.toPython()

    # ACTION 3
    # Examples of direct portfolio data queries
    # Get data for an obligor with arbitrary ID
    query = '2486'
    obligor_data = get_data(portfolio_url, query)
    print("--- Action 3: print selected portfolio data ---")
    print("EAD = ", obligor_data['EAD'])

    # Get a certain page (for large portfolios)
    query = '?page=20'
    obligor_data = get_data(portfolio_url, query)

    # Get the data in descenting exposure value
    query = '?sort=-EAD'
    obligor_data = get_data(portfolio_url, query)

    # ACTION 4
    # Construct and post a calculation ticket
    ticket = {}
    # 0 "Authentication step"
    ticket["user_id"] = "User001"
    # 1 Select which portfolio to use (based on URI + filtering)
    query = '?page=21'
    ticket["portfolio_url"] = portfolio_url + query
    # 2 Select where to store output (here: we take the server suggestion)
    ticket["output_url"] = output_url
    # 3 Send model url
    ticket["model_url"] = model_url

    print("--- Action 4a: print calculation ticket as seen by server ---")
    calculation_info = post_calculation_ticket(model_url, ticket)
    print("--- Action 4b: print output info as sent to client ---")
    print(calculation_info.json())

    # ACTION 5
    # Explore Results
    result_url = calculation_info.json()['output_url']
    results = get_results(result_url)
    print("--- Action 5: print results ---")
    print("The result of " + model_name + " applied to " +
          portfolio_url + query + " is: ")
    print(results)
