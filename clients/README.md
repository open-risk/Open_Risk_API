## API Explorer (Python Client)

The API Explorer is a python based client for exploring the Open Risk Models API.
The assumption below is that you are using the client together with the other bundled servers without
modifying any of the url data. 

### Getting started

#### Startup the demo resource servers:

- Model Server: Follow the instructions or the [model server](https://github.com/open-risk/Open_Risk_API/tree/master/model_server)  	
- Data Server: Follow the instructions for the [data server](https://github.com/open-risk/Open_Risk_API/tree/master/data_server). 

Both servers rely on an underlying MongoDB database. This database must be populated with a portfolio database for the demo to work (see data server documentation
for the details)
  
#### Run the client script:

Simply run the script from the console (python explorer.py) or in a python interpreter

There is no error checking at present

#### Action 1: Exploring the registry

The first example illustrates how to start exploring the API from its entry point. In this demo for simplicity the registry server is also emulated by the model server. The GET request returns a JSON-LD document which is parsed to return the URL's and names of available models.

#### Action 2: Print selected model data

The second example illustrates how to use the data extracted previously to obtain more information about the models. You select the desired model by name and request further model info which is returned in JSON-LD
format and printed out as a set of graph nodes. We parse this graph to store the URI's for portfolio data and for output data.

#### Action 3: Direct access to portfolio data

The third set of examples illustrates how to directly extract data from the data server. To work with data we construct a simple or more elaborate query using the Eve query syntax (mongodb query syntax is also supported). Please note that mongodb data are served paginated by default. The following examples should give adequate flavor how to query the database

- uri/obligors/data_id selects single data point
- uri/obligors/?page=page_id selects single page of data
- uri/obligors/?max_results=100&page=2  sets the page size to 100 and selects the second page
- uri/obligors/?sort=field sorts the data by field
- uri/obligors/?where=field=="value" select data where given field has desired value
- uri/obligors/?where={"field": "value"} alternative syntax for the same

#### Action 4: Setup a calculation

Setting up a calculation requires compiling a "ticket" (a python dict structure within this client). The ticket has the following items:

- user_id (foobar)
- portfolio url
- output url (foobar)
- model url

The calculation ticket is posted as JSON payload to the model url

Please note that while we specify an output_url this is for forward compatibility, in the current implementation the model server will decide autonomously where to store the results (and send us back the link)

The calculation result info sent back to the user is a JSON object

- user_id (foobar0
- output url in the following format: /modelserver/models/model_name/calc_id

#### Action 5: "Explore" a calculation

The client parses the result info and GET's the actual result from the supplied URL
