# 
# Author: Nate Winneg
# Date: 2023-02-04
#
# Function functions to parse Capital One credit card data files

import numpy as np
import pandas as pd

def computeCosts(fpath):
    # fpath = basePath+year+'/'+month+'/'+card+'_'+month.lower()+year[2:len(year)]+'.csv'
    data = pd.read_csv(fpath)
    numTrans = data.shape[0]

    grocery = np.array([])
    merch = np.array([])
    dining = np.array([])
    auto = np.array([])
    misc = np.array([])
    for nn in range(numTrans):
        r = data.iloc[nn,:] 
        # Groceries: Trader joes comes up as merch
        if ('TRADER' in r.Description) or ('Grocery' in r.Category) or ('WEGMANS' in r.Description):
            grocery = np.append(grocery,nn)
        # Merchandise: Trader joes again
        elif ('Merch' in r.Category) and ('TRADER' not in r.Description):
            merch = np.append(merch,nn)
        # Dining
        elif ('Dining' in r.Category):
            dining = np.append(dining,nn)
        # Gas and other automotive stuff
        elif ('Auto' in r.Category):
            auto = np.append(auto,nn)
        # Don't count credit payments
        elif (np.isnan(r.Debit)):
            continue
        # Catch all for anything else
        else:
            misc = np.append(misc,nn)

    dataOrganized = {
        "Groceries": sum(data.iloc[grocery,:].Debit),
        "Merchandise": sum(data.iloc[merch,:].Debit.iloc[np.array(np.invert(np.isnan(data.iloc[merch,:].Debit)),dtype='bool')]),
        "Dining Out": sum(data.iloc[dining,:].Debit.iloc[np.array(np.invert(np.isnan(data.iloc[dining,:].Debit)),dtype='bool')]),
        "Gas/Auto": sum(data.iloc[auto,:].Debit.iloc[np.array(np.invert(np.isnan(data.iloc[auto,:].Debit)),dtype='bool')]),
        "Other": sum(data.iloc[misc,:].Debit.iloc[np.array(np.invert(np.isnan(data.iloc[misc,:].Debit)),dtype='bool')]),
    }

    return dataOrganized
        
def getSpotify(fpath):
    # fpath = basePath+year+'/'+month+'/'+card+'_'+month.lower()+year[2:len(year)]+'.csv'
    data = pd.read_csv(fpath)

    gData = data.iloc[np.array(np.invert(np.isnan(data.Debit)),dtype='bool')]

    desc = gData.Description
    sIdx = np.array(desc.str.find('Spotify') + 1,dtype=bool)

    sData = gData.Debit.iloc[sIdx]

    return sum(sData)

def getCardNumber(fpath):
    # Get the card number
    data = pd.read_csv(fpath)
    cardNumber = data.iloc[1,2]

    return cardNumber
