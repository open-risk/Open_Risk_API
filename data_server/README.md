## API Demo (Data Server)

The API Explorer is a python based client for exploring the Open Risk Models API.
The assumption below is that you are using the client together with the other bundled servers without
modifying any of the url data. 

### Getting started

#### Setting up MongoDB as backend

To run the data server we must first install MongoDB. The default port is assumed, otherwise adjust the settings.py file. 

Check that the server is running and accessible via http by pointing your browser to http://localhost:28017/

#### Creating a database with mock credit data

Once mongodb is up and running we need to create some data. The following script executed inside a mongodb shell will give us plenty of data to play with. Please note that we overwrite the _id field for simplicity

```
use eve
db.createCollection("obligors")

function create_portfolio() {
    for ( i =1; i<= 100000; i++)
       db.obligors.insert({ id : i, EAD : Math.random(), PD : Math.random(), LGD : Math.random()})
}

create_portfolio()
```

Check that the creation went smoothly by listing the obligor data within the mongodb shell:

```
db.obligor.find()
```

### Setting up the data server:

#### Dependencies

The data server is based on the python-eve framework (in turn based on flask). 

- Pip install eve 

#### Starting up the data server

The whole setup is captured by two files, the run.py and settings.py files

- Simply run the data server script from the console (python run.py)
- You can check the data server is live by pointing your browser to the port http://127.0.0.1:5011/
- In the following URL  http://127.0.0.1:5011/obligors you should get an xml reply with some datasets
- or by using curl from the console (curl -v http://127.0.0.1:5011/)
  
