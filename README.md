# Open Risk API
An API for interconnected risk models and risk data

![](https://github.com/open-risk/Open_Risk_API/blob/master/Architecture.png)

The Open Risk API is an open source application programming interface (API) that allows for the distributed development, deployment and use of financial risk models. The proposal targets the following key problem: how to integrate in a robust and trustworthy manner diverse risk modeling and risk data resources, contributed by multiple authors, using different technologies, and which very likely will evolve over time. 

The API builds on and integrates two key frameworks, Semantic Data and RESTful API's

A white paper with the current specification of the API is available [here](https://www.openriskmanagement.com/wp-content/uploads/2016/02/OpenRiskWP03_053115.pdf)

# Demo Implementation

We illustrate the API with an open source implementation that takes a use case from the analysis of credit risk in loan portfolios. The implementation consists of demo model / data servers and clients implemented using Python and MongoDB. 

There are further dependencies on flask and python-eve

### Contributions

We welcome contributions to the Open Risk API in terms of ideas or code