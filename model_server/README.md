## API Demo (Model Server)

The API Demo Model Server is a python based server for exploring the Open Risk Models API.

The assumption below is that you are using the client together with the other bundled servers without modifying any of the url data. 

### Getting started


#### Dependencies

The server is based on the python flask framework. It has the following additional dependencies

- pip install requests
- pip install numpy
- pip install rdflib
- pip install rdflib-jsonld

#### Install a model library

This demo is using a library of concentration risk measures. You can get a copy here https://github.com/open-risk/concentration_library

You only need to include the file concentration_library.py (for convenience we include it in this demo)

#### Startup the model server:
   	
- Simply run the server script from the console (python model_server.py)
- The model server should startup on port http://127.0.0.1:5012/
- You can check the server is live by pointing your browser to the port (you will get an json-ld reply)
- or by using curl from the console (curl -v http://127.0.0.1:5012/)
  
#### About the model server:

- In this demo the model metadata are stored in-memory for simplicity. 
- In production they would be obtained through a document store (Model metadata are stored as an RDF graph and manipulated using rdflib)

#### Model Server API endpoints: 

The general structure is

- /
- /models
- /models/{model_name}
- /models/{model_name}/{calc_id}

NB: In the demo only /models/hhi and /models/shannon are available

The first two endpoints are conflated and return the model description list. The parametrized model_name endpoint serves model metadata via GET and accepts calculation tickets via POST
The calculation_id resource is created when a valid calculation ticket is posted.

#### Metadata format

The model metadata are in JSON-LD format. This is human readable with any JSON editor

### Calculation Storage

- The model server stores calculation inputs and results in a mongodb instance (calculations database)
- The default URL (mongodb://localhost:27017/) is hardwired, you need to change if your installation differs
- The input tickets are stored in the calculations.inputs collection
- The output results are stored in calculations.outputs and are available at the <calc_id> endpoint