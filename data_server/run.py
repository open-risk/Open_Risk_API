# (c) 2015 - 2023 Open Risk (https://www.openriskmanagement.com)

# -*- coding: utf-8 -*-
"""
Created on Mon May  4 16:33:42 2015
@author: Open Risk
"""

from eve import Eve

app = Eve(settings="settings.py")

if __name__ == '__main__':
    app.run(port=5011)
