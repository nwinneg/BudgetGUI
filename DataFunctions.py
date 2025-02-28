import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import bofaTools
import capitalOneTools
import venmoTools_v2

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

def getAvailableMonths(fpath,cardType):

    if cardType == "BofA":
        df = pd.read_csv(fpath,skiprows=6)
    elif cardType == "Venmo":
        df = pd.read_csv(fpath,skiprows=2)
    else:
        df = pd.read_csv(fpath)
    
    if cardType == "Venmo":
        datetimes = pd.to_datetime(df["Datetime"].dropna())
        datetimes = datetimes.dt.strftime('%b-%y')
        return datetimes.iloc[0]
    elif cardType == "BofA":
        dates = pd.to_datetime(df["Date"])
        dates = dates.dt.strftime('%b-%y')
        return list(dates.unique())
    elif (cardType == "Savor") or (cardType == "Journey"):
        dates = pd.to_datetime(df["Transaction Date"])
        dates = dates.dt.strftime('%b-%y')
        return list(dates.unique())
    elif (cardType == "Sapphire"):
        dates = pd.to_datetime(df["Transaction Date"])
        dates = dates.dt.strftime('%b-%y')
        return list(dates.unique())
    
def calculateCosts(fileList,cardTypes,month,costSheet,transactionSheet):
    # Function does the following: 
    #   Loops through files
    #   Calculates costs and adds them to the cost sheet
    #   Builds a complete list of transactions in selected month and populates the table
    
    transTable = pd.DataFrame(columns=["Account","Description","Date","Cost"])

    for ff in range(len(fileList)):
        fpath = fileList[ff]
        cardType = cardTypes[ff]

        if cardType == "BofA":
            pass
        elif cardType == "Venmo":
            # Get the data
            data = venmoTools_v2.getVenmoData(fpath,month)
            if data is None:
                continue
            data["Account"] = "Venmo"
            rentCost = venmoTools_v2.getRentVenmo(fpath)
            vNet = venmoTools_v2.venmoCompute(fpath,month)
            
            # Populate cost sheet
            costSheet.data["Rent"]= str(-rentCost)
            costSheet.data["Venmo Bofa Net"] = str(-vNet)
            costSheet.updateTotal()
            costSheet.setData()

            # fdata = venmoTools_v2.venmoData(fpath)
            # print(rentCost)
            # print(fdata)
        elif cardType == "Savor":
            pass
        elif cardType == "Journey":
            # Get spotify
            spotifyCost = capitalOneTools.getSpotify(fpath)
            costSheet.data["Spotify"] = str(spotifyCost)

            # Get additional
            data = capitalOneTools.computeCosts(fpath)

            # TODO: Function to make transaction table
            

            # Add to table
            print('Spotify {}'.format(spotifyCost))
            print(data)
            # print(data['Groceries'])
            # print(data['Merchandise'])
            # print(data['Dining Out'])
            # print(data['Gas/Auto'])
            # print(data['Other'])

        elif cardType == "Sapphire":
            pass
            
        
        # transTable = pd.concat([transTable,data],ignore_index=True)
        # transactionSheet.updateSheet(transTable.sort_values(by='Date'))


            
