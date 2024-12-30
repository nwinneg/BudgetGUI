import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def getAccountType(fpath): # Read the file to check what kind of file this is
    # Read in the csv file
    data = pd.read_csv(fpath,nrows=1)
    headers = data.columns.tolist()

    # Check if bofa
    if ("Beginning balance" in data.iloc[0,0]):
        return "BofA"
    
    # Ok not bofa
    data = pd.read_csv(fpath)
    headers = data.columns.tolist()

    # Check if Venmo
    venmoCheck = "Account Statement"
    if (venmoCheck in headers[0]):
        return "Venmo"

    # Check for Capital One
    if ("Card No." in headers):
        cardNo = data["Card No."][0]
        if cardNo == 5577:
            return "Savor"
        elif cardNo == 8949:
            return "Journey"
    
    # If we've gotten to here, it's chase [For Now]
    return "Sapphire"
    
