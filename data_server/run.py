# -*- coding: utf-8 -*-
"""
Created on Mon May  4 16:33:42 2015
@author: OpenRisk
"""

from eve import Eve
app = Eve(settings="settings.py")

if __name__ == '__main__':
    app.run(port=5011)
