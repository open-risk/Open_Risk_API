# add dictionary schema
# dictionaries/dictionary_name endpoint

# ISSUES datetime type not serialized to json

obligor_schema = {
    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/nicolaiarocci/cerberus) for details.
    'id': {
        'type': 'integer',
        'required': True,
        'unique': True,
    },
    'EAD': {
        'type': 'float',
    },
    'PD': {
        'type': 'float',
    },
    'LGD': {
        'type': 'float',
    },
}

# endpoints

obligors = {
    # 'title' tag used in item links. Defaults to the resource title minus
    # the final, plural 's' (works fine in most cases but not for 'people')
    'item_title': 'obligor',

    # by default the standard item entry point is defined as
    # '/obligors/<ObligorId>'.

    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'id'
        },

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST', 'DELETE'],

    'schema': obligor_schema
}

DOMAIN = {
    'obligors': obligors,
}
MONGO_HOST = 'localhost'
MONGO_PORT = 27017

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

DEBUG = 'True'