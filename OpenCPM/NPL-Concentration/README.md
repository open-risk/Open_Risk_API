## OpenCPM Demo (Model Server)

The **OpenCPM Demo Model Server** is a python/flask based server for exploring a simplified version of the [Open Risk API](https://www.openriskmanagement.com/open-risk-api/).


### Getting started

The repo aims to provide a self-contained demo. 

- Clone the repo in your local environment
- Create a virtual environmennt
- Install the dependencies
- Install a model library
- Startup a model server
- Explore the endpoints

#### Dependencies

The server is based on the python flask framework. It has some additional dependencies (numpy, pandas, rdflib) that are easily installed with pip:

```shell
  pip install -r requirements.txt
```

#### Installing a "model" library

This demo is using a concentrationMetrics, a library of concentration risk measures. You can get a copy of the [latest version here](https://github.com/open-risk/concentrationMetrics)

* You only need to include the file model.py (for convenience we include it in this demo)
* The list of available models is in model_list.rdf
* The model metadata are stored in one rdf file per model (HHI_Index.rdf, Gini_Index.rdf etc)


#### Startup the model server
   	
Run the server script from the console

```shell
    python Model_Server.py
```

- The model server should startup on port http://127.0.0.1:5000/
- You can check the server is live by pointing your browser to the port (you will get as a response a json-ld reply). 
  
You can also query the API using curl from the console (curl -v http://127.0.0.1:5000/)

#### Model Server API endpoints

The general structure of the simplified API is

- /
- /model_list
- /{model_name}

The model name endpoint responds to both GET / PUT http verbs. In the first instance
it returns model metadata. In the second instance it returns the model output

The model metadata are in JSON-LD format. This format is human readable and can be edited with any IDE / JSON editor