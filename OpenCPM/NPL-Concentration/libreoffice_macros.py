# encoding: utf-8

# (c) 2018 Open Risk, all rights reserved
#
# Concentration Library is licensed under the MIT license a copy of which is included
# in the source distribution of TransitionMatrix. This is notwithstanding any licenses of
# third-party software included in this distribution. You may not use this file except in
# compliance with the License.
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.

"""

This file contains python macros to enable the libreoffice calc application
to connect to a model server conforming to the Open Risk API as a client

"""

import uno
import json
import requests

oDoc = XSCRIPTCONTEXT.getDocument()


# This macro interrogates the API to obtain basic help (here the model list)
def model_list_request():
    oSheet = oDoc.createInstance( "com.sun.star.sheet.Spreadsheet" )
    oDoc.Sheets.insertByName( "Output", oSheet )    
    r = requests.get('http://127.0.0.1:5000/model_list/')  
    data = r.json()   
    Offset = 1
    j = 1
    for item in data:
        oCell1 = oSheet.getCellByPosition(1, Offset + j - 1)     
        oCell1.String = item
        j += 1


# This function creates a json structure out of the desired input dataset
def create_payload(Dimension, dSheet):

    oCell = dSheet.getCellRangeByName("K1")
    oCell.String = Dimension

    # find last populated row / length of consolidated dataset
    oCursor = dSheet.createCursor()
    oCursor.gotoEndOfUsedArea(False)
    LastRow= oCursor.RangeAddress.EndRow
    LastRow += 1
    Y_Offset = 3
    X_Offset = 0
    N = LastRow - Y_Offset
    
    x = []
    y = []
    
    for j in range(1,N + 1):    
        oCell = dSheet.getCellByPosition(X_Offset + 1, Y_Offset + j - 1)
        lID = oCell.Value
        oCell = dSheet.getCellByPosition(X_Offset + 2, Y_Offset + j - 1)
        nuts = oCell.String
        oCell = dSheet.getCellByPosition(X_Offset + 3, Y_Offset + j - 1)
        nace = oCell.String
        oCell = dSheet.getCellByPosition(X_Offset + 4, Y_Offset + j - 1)
        balance = oCell.Value
        if Dimension == 'LOAN':
            x.append(lID)
        elif Dimension == 'NACE':
            x.append(nace)
        elif Dimension == 'NUTS':
            x.append(nuts)
        y.append(balance)

    data = {'x': x, 'y' : y}
    data = json.dumps(data)
    return data


# This macro initiates the calculation request
# A number of inputs are hardwired in this demo version
# The creation of the payload from the consolidated data sheet is
# implemented in a separate function (create_payload)
def calculation_request(user):
    
    # Select which dimension and which index to use
    iSheet = oDoc.getSheets().getByName('Control') 
    # Dimension: LOAN, NACE, NUTS
    oCell = iSheet.getCellRangeByName("C5")
    Dimension = oCell.String
    
    # This must correspond to an available model in the model server
    # 'Gini_Index', 'HHI_Index', 'Shannon_Index'
    oCell = iSheet.getCellRangeByName("C6")  
    Model = oCell.String
            
    headers = {'content-type': 'application/json'}
    url = 'http://127.0.0.1:5000/' + Model
    
    dSheet = oDoc.getSheets().getByName('Data Summary') 
    data = create_payload(Dimension, dSheet)
    
    # r = requests.get(url)  
    r = requests.post(url, data=data, headers=headers)    
    data = r.json()   
    
    # report results
    oCell = iSheet.getCellRangeByName("F5")
    oCell.String = Model
    oCell = iSheet.getCellRangeByName("G5")
    oCell.String = Dimension
    oCell = iSheet.getCellRangeByName("H5")
    oCell.Value = data[Model]
    

# This macro consolidates the data required for a concentration risk calculation into a new sheet
# Reinforcing separation of concerns, the client does not perform any business logic (processing of data)
# except possibly converting to a more suitable format
def consolidate_data(user):
    
    # create data summary sheet
    try:
        dSheet = oDoc.getSheets().getByName('Data Summary') 
        dSheet.clearContents(5)
    except:
        dSheet = oDoc.createInstance( "com.sun.star.sheet.Spreadsheet" )
        oDoc.Sheets.insertByName( "Data Summary", dSheet )
        
    # select relevant sheets
    ws1 = oDoc.getSheets().getByName('3. Counterparty ')
    ws2 = oDoc.getSheets().getByName('4. Relation (Borrower-Loan)')
    ws3 = oDoc.getSheets().getByName('7. Loan')
    
    # find last populated row / length of dataset
    oCursor = ws1.createCursor()
    oCursor.gotoEndOfUsedArea(False)
    LastRow= oCursor.RangeAddress.EndRow
    LastRow += 1
    Y_Offset = 3
    X_Offset = 0
    N = LastRow - Y_Offset

    # extract counterparty ID data
    id_list = []    
    for j in range(1,N + 1):
    # Counterparty identifier
        oCell = ws1.getCellByPosition(1, Y_Offset + j - 1)
        ID = oCell.Value
        id_list.append(ID)
        
    # extract counterparty region data
    region_list = []    
    for j in range(1,N + 1):
    # Counterparty identifier
        oCell = ws1.getCellByPosition(19, Y_Offset + j - 1)
        nuts = oCell.String
        region_list.append(nuts)

    # extract counterparty sector data
    sector_list = []    
    for j in range(1,N + 1):
    # Counterparty identifier
        oCell = ws1.getCellByPosition(27, Y_Offset + j - 1)
        nace = oCell.String
        sector_list.append(nace)
        
    # extract loan ID data
    loan_list = []    
    for j in range(1,N + 1):
    # Counterparty identifier
        oCell = ws2.getCellByPosition(1, Y_Offset + j - 1)
        ID = oCell.Value
        loan_list.append(ID)        
        
    # extract loan balance data
    balance_list = []    
    for j in range(1,N + 1):
    # Counterparty identifier
        oCell = ws3.getCellByPosition(23, Y_Offset + j - 1)
        balance = oCell.Value
        balance_list.append(balance)   
            
    # report portfolio size
    oCell = dSheet.getCellRangeByName("A1")
    oCell.String = "Portfolio Size"
    oCell = dSheet.getCellRangeByName("B1")
    oCell.Value = N
    
    j = 0
    # label columns    
    oCell = dSheet.getCellByPosition(X_Offset, Y_Offset + j - 1)
    oCell.String = "Counterparty ID"
    oCell = dSheet.getCellByPosition(X_Offset + 1, Y_Offset + j - 1)
    oCell.String = "Loan ID"
    oCell = dSheet.getCellByPosition(X_Offset + 2, Y_Offset + j - 1)
    oCell.String = "NUTS Code"
    oCell = dSheet.getCellByPosition(X_Offset + 3, Y_Offset + j - 1)
    oCell.String = "NACE Code"
    oCell = dSheet.getCellByPosition(X_Offset + 4, Y_Offset + j - 1)
    oCell.String = "Loan Balance"
    
    for j in range(1,N + 1):
    # Save counterparty identifier
        cID = id_list[j-1]
        lID = loan_list[j-1]
        nuts = region_list[j-1]
        nace = sector_list[j-1]
        balance = balance_list[j-1]
        oCell = dSheet.getCellByPosition(X_Offset, Y_Offset + j - 1)
        oCell.Value = cID
        oCell = dSheet.getCellByPosition(X_Offset + 1, Y_Offset + j - 1)
        oCell.Value = lID
        oCell = dSheet.getCellByPosition(X_Offset + 2, Y_Offset + j - 1)
        oCell.String = nuts
        oCell = dSheet.getCellByPosition(X_Offset + 3, Y_Offset + j - 1)
        oCell.String = nace
        oCell = dSheet.getCellByPosition(X_Offset + 4, Y_Offset + j - 1)
        oCell.Value = balance
