## API Demo (Data Server)

The API Explorer is a python based client for exploring the Open Risk Models API.
The assumption below is that you are using the client together with the other bundled servers without
modifying any of the url data. 

### Getting started

#### Setting up the data server directory

The server is based on the python-eve framework (in turn based on flask). The whole setup is captured
by two files, the run.py and settings.py files


#### Setting up MongoDB

To run the data server we must install MongoDB. The default port is assumed, otherwise adjust the settings.py
file. 

Check that the server is running and accessible via http by pointing your browser to http://localhost:28017/

#### Creating the database

Once mongodb is up and running we need to create some data. The following script executed inside a mongodb
shell will give us plenty of data to play with. Please note that we overwrite the _id field for simplicity

```
db.createCollection("obligors")

function create_portfolio() {
    for ( i =1; i<= 100000; i++)
       db.obligors.insert({ _id : i, EAD : Math.random(), PD : Math.random(), LGD : Math.random()})
}

create_portfolio()
```


#### Startup the data server:
   	
- Simply run the server script from the console (python run.py)
- The data server should startup on port http://127.0.0.1:5011/
- You can check the server is live by pointing your browser to the port (you will get an xml reply)
- or by using curl from the console (curl -v http://127.0.0.1:5011/)
  
