#!"C:\Python27\ArcGIS10.7\python.exe"
#requires ArcGIS python 2

import pandas as pd
try:
    from Tkinter import Tk
except ImportError:
    from tkinter import Tk

# In Infoworks ICM: validate the network, right click anywhere in the validation output window, and click "Copy to clipboard"

def uniqueFromField(pdf, fieldName):
    '''
    Inputs:
    pdf = the Pandas Dataframe to work with
    fieldName = Field Name (Table Heading) from the InfoWorks Validation Error Output Window (selected in tkinter dropdown) 
    
    Outputs:
    Returns a list of unique values in the rows under the column for the field name selected (Selects the column in the table for further analysis).
    '''
    return pdf.loc[:,fieldName].unique().tolist()

def filterBySelection(pdf, fieldName, rowName):
    '''
    Inputs:
    pdf = The Pandas Dataframe to work with
    fieldName = Field Name (Table Heading) from the InfoWorks Validation Error Output Window (selected in tkinter dropdown)
    rowName = Row name under the specified field from the InfoWorks Validation Error Output Window (selected in tkinter dropdown)
    
    Outputs:
    A Pandas dataframe where the criteria is met that the data under the column 'fieldName' is equal to 'rowName'.
    '''
    return pdf.loc[pdf[fieldName] == rowName]

def pdfToSql(pdf, objectType):
    '''
    Inputs:
    pdf = The Pandas Dataframe to work with, filtered so that only the network objects of interest will be included in the output SQL Query
    
    Outputs:
    A string of text that was copied to the clipboard (and can be pasted into the ICM SQL Query Tool).
    '''
    if objectType == 'Conduit':
        tableWithSQL = pdf.loc[pdf.loc[:,'Object Type'] == 'Conduit'].assign(SQLText = "oid = '" + pdf.Object + "' OR ")
        initString = str(tableWithSQL.loc[:,'SQLText'].to_string(index = False))
        stringFinal = 'SELECT ALL WHERE \n' + initString[:-3]
    elif objectType == 'Node':
        tableWithSQL = pdf.loc[pdf.loc[:,'Object Type'] == 'Node'].assign(SQLText = "oid = '" + pdf.Object + "' OR ")
        initString = str(tableWithSQL.loc[:,'SQLText'].to_string(index = False))
        stringFinal = 'SELECT ALL WHERE \n' + initString[:-3]
    elif objectType == 'Subcatchment':
        tableWithSQL = pdf.loc[pdf.loc[:,'Object Type'] == 'Subcatchment'].assign(SQLText = "subcatchment_id = '" + pdf.Object + "' OR ")
        initString = str(tableWithSQL.loc[:,'SQLText'].to_string(index = False))
        stringFinal = 'SELECT ALL WHERE \n' + initString[:-3]
    print
    print "There were " + str(len(tableWithSQL.index)) + " records in the selection"
    return stringFinal

ICM_Clipboard = pd.read_clipboard(header = None, names=['Code', 'Priority', 'Object Type', 'Object', 'Field', 'Scenario', 'Message']) #Extracts the clipboard from ICM and converts it to a Pandas Dataframe with appropriate headings

if len(pd.read_clipboard(header = None).columns) == 7:

    fieldOptions = [ 'Code', 'Priority', 'Object Type', 'Object', 'Field', 'Scenario', 'Message' ]
    objectTypes = ['Conduit', 'Node', 'Subcatchment']

    for i in fieldOptions:
        print (i)
    print
    
    fieldName = raw_input("Which column do you want to filter? ")

    uniqueValList = uniqueFromField(ICM_Clipboard, fieldName)

    print
    for i in uniqueValList:
        print (i)
    print
    
    rowName = raw_input("Which value do you want to filter for? ")

    NewICM_Clipboard = filterBySelection(ICM_Clipboard, fieldName, rowName)

    print
    for i in objectTypes:
        print (i)
    print

    objectType = raw_input("Which Object Type do you want to filter? ")

    strToExport = pdfToSql(NewICM_Clipboard, objectType)

    #BEGIN: Code to copy text to the clipboard
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(strToExport)
    r.update()
    r.destroy()
    #END: Code to copy text to the clipboard
    
    print
    print(strToExport)
    print
    raw_input("Press Enter to copy SQL text to keyboard and exit this program")
else:
    print("Need to copy ICM validation output table to clipboard before running this program!")
    while True:
        raw_input()
