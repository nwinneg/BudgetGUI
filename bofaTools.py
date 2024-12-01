# 
# Author: Nate Winneg
# Date: 2023-02-04
#
# Function functions to parse Bank of America data files

import numpy as np
import pandas as pd

# basePath = 'C:/Users/nwinn/Desktop/Budget/data/'

def getSummary(fpath):
    # fpath = basePath+year+'/'+month+'/BOFA_'+month.lower()+year[2:len(year)]+'.csv'
    hdata = pd.read_csv(fpath,skiprows=1,nrows=4,header=None)
    return hdata.iloc[:,[0,2]]

def getEversource(fpath):
    # fpath = basePath+year+'/'+month+'/'+'BOFA'+'_'+month.lower()+year[2:len(year)]+'.csv'

    data = pd.read_csv(fpath,skiprows=6)

    desc = data.Description
    test = np.array(desc.str.find('EVERSOURCE') + 1,dtype=bool)

    eData = data.iloc[test,:]

    eCost = np.array(eData.Amount,dtype='float')
    
    myCost = sum(eCost)/2.

    return myCost

def getTravelers(fpath):
    # fpath = basePath+year+'/'+month+'/'+'BOFA'+'_'+month.lower()+year[2:len(year)]+'.csv'

    data = pd.read_csv(fpath,skiprows=6)

    desc = data.Description
    test = np.array(desc.str.find('TRAVELERS') + 1,dtype=bool)

    cData = data.iloc[test,:]

    cCost = np.array(cData.Amount,dtype='float')
    
    myCost = sum(cCost)

    return myCost

def getAstound(fpath):
    data = pd.read_csv(fpath,skiprows=6)

    # Get RCN Specific rows
    desc = data.Description
    test = np.array(desc.str.find('RCN') + 1,dtype=bool)
    cData = data.iloc[test,:]

    cCost = np.array(cData.Amount,dtype='float')

    myCost = -sum(cCost)

    return myCost


