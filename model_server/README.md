## API Demo (Model Server)

The API Demo Model Server is a python based server for exploring the Open Risk Models API.

The assumption below is that you are using the client together with the other bundled servers without
modifying any of the url data. 

### Getting started

#### Setting up the model server directory

The server is based on the python flask framework

#### Startup the model server:
   	
- Simply run the server script from the console (python model_server.py)
- The model server should startup on port http://127.0.0.1:5012/
- You can check the server is live by pointing your browser to the port (you will get an json-ld reply)
- or by using curl from the console (curl -v http://127.0.0.1:5012/)
  
#### About the model server:

- The model metadata is in memory for simplicity. In production this would be a document store
- Model metadata are stored as an RDF graph and manipulated using rdflib

### API endpoints: 

- /
- /models
- /models/{model_name}
- /models/{model_name}/{calc_id}

The first two are conflated and return the model description list
The parametrized model_name endpoint serves model metadata via GET and accepts calculation tickets via POST
The calculation_id resource is created when a valid calculation ticket is posted

### Calculation Storage

- The model server stores calculation inputs and results in a mongodb instance (calculations database)
- The default URL (mongodb://localhost:27017/) is hardwired, you need to change if your installation differs
- The input tickets are stored in the calculations.inputs collection but are not accessible in the current implementation
- The output results are stored in calculations.outputs and are available at the <calc_id> endpoint