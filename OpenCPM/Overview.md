## API Overview

This is the high level overview of the input / output interaction between 
the different OpenCPM application components:

### Applications / modules

The following lists the key inputs (I) and outputs (O) of all modules
 
#### A1 Simulation Engine (C++ based):

This is the core simulation (scenario) engine. 

* A1_I1 Engine receives model configuration files
* A1_I2 Engine receives portfolio data
* A1_I3 Engine receives use scenario data
* A1_O1 Engine emits numerical outputs

#### A2 model configurator (CLI/GUI application):

- A2_I1 receives model configuration files (possibly empty)
- A2_O1 emits model configuration files

#### A3 portfolio creator (CLI/GUI):

- A3_I1 receives starting portfolio data (possibly empty)
- A3_O1 emits output portfolio data

#### A4 portfolio visualizer:

- A4_I1 receives portfolio data
- A4_O1 emits portfolio graphics outputs (histograms, pie-charts etc)

#### A5 portfolio explorer / summarizer:

- A5_I1 receives portfolio data
- A5_O1 emits portfolio numerical outputs (tables with statistics etc.)

#### A6 risk visualizer:

- A6_I1 receives model outcomes data
- A6_O1 produces model outcomes graphics output (loss distributions, heat-maps etc.)

#### A7 risk report creator:

- A7_I1 receives graphics outputs
- A7_I2 receives numerical outputs
- A7_O1 emits textual reports (html, pdf)


### Database API's:

#### D1 portfolio database:

- receives portfolio snapshot data
- updates portfolio database
- extracts portfolio snapshot data from portfolio database

#### D2 calculation database:

- receives calculation data
- updates calculation database
- extract calculation data from calculation database