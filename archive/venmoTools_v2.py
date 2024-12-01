# 
# Author: Nate Winneg
# Date: 2023-09-01
#
# Function functions to parse venmo data files

import pandas as pd
import numpy as np

def venmoCompute(fpath):
    landlord = 'Wafa El Awar'
    # vfile = basePath+year+'/'+month+'/Venmo_'+month.lower()+year[2:len(year)]+'.csv'

    rdata = pd.read_csv(fpath,skiprows=2)
    # remove nan type rows, standard transfers, rent, (Internet now included in venmo)
    toDrop = np.array([])
    for row in range(rdata.shape[0]):
        if type(rdata.Type[row]) != str:
            toDrop = np.append(toDrop,row)
        elif rdata.Type[row] == 'Standard Transfer':
            toDrop = np.append(toDrop,row)
        elif rdata.To[row] == landlord:
            toDrop = np.append(toDrop,row)
            
    rdata = rdata.drop(toDrop)

    tdata = rdata["Amount (total)"]
    fdata = np.zeros(tdata.shape[0])
    for row in range(tdata.shape[0]):
        tmp = pd.to_numeric(tdata.iloc[row].replace('$','').replace(' ','').replace(',',''))
        fdata[row] = tmp

    vSum = fdata.sum()

    return vSum

def getWifi(fpath):
    # Check for reasonably named wifi charge
    rdata = pd.read_csv(fpath,skiprows=2)
    wifiCost = 0
    tdata = rdata["Amount (total)"]
    for row in range(rdata.shape[0]):
        if 'inter' in str(rdata.Note[row]).lower():
            wifiCost = pd.to_numeric(tdata.iloc[row].replace('$','').replace(' ','').replace(',',''))
    if abs(wifiCost) > 10 and abs(wifiCost) < 35:
        pass
    else:
        wifiCost = 0
    return wifiCost
    

def venmoData(fpath):
    landlord = 'Wafa El Awar'
    # vfile = basePath+year+'/'+month+'/Venmo_'+month.lower()+year[2:len(year)]+'.csv'
    rdata = pd.read_csv(fpath,skiprows=2)
    
    # remove nan type rows, standard transfers, rent, (Internet now included in venmo)
    toDrop = np.array([])
    for row in range(rdata.shape[0]):
        if type(rdata.Type[row]) != str:
            toDrop = np.append(toDrop,row)
        elif rdata.Type[row] == 'Standard Transfer':
            toDrop = np.append(toDrop,row)
        elif rdata.To[row] == landlord:
            toDrop = np.append(toDrop,row)
            
    rdata = rdata.drop(toDrop)

    tdata = rdata["Amount (total)"]
    fdata = np.zeros(tdata.shape[0])
    for row in range(tdata.shape[0]):
        tmp = pd.to_numeric(tdata.iloc[row].replace('$','').replace(' ','').replace(',',''))
        fdata[row] = tmp

    return fdata