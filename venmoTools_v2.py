# 
# Author: Nate Winneg
# Date: 2023-09-01
#
# Function functions to parse venmo data files

import pandas as pd
import numpy as np

def venmoCompute(fpath,month):
    landlord = 'Wafa El Awar'

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

    tmp = pd.to_datetime(rdata["Datetime"])
    tmp = tmp.dt.strftime('%b-%y')
    if tmp.iloc[0] != month:
        return 0

    tdata = rdata["Amount (total)"]
    fdata = np.zeros(tdata.shape[0])
    for row in range(tdata.shape[0]):
        tmp = pd.to_numeric(tdata.iloc[row].replace('$','').replace(' ','').replace(',',''))
        fdata[row] = tmp

    vSum = fdata.sum()

    return vSum

def getWifi(fpath): # Deprecated
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

def venmoData(fpath,month):
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

    tmp = pd.to_datetime(rdata["Datetime"])
    tmp = tmp.dt.strftime('%b-%y')
    if tmp.iloc[0] != month:
        return 0

    tdata = rdata["Amount (total)"]
    fdata = np.zeros(tdata.shape[0])
    for row in range(tdata.shape[0]):
        tmp = pd.to_numeric(tdata.iloc[row].replace('$','').replace(' ','').replace(',',''))
        fdata[row] = tmp

    return fdata

def getVenmoNet(fpath,month):
    rdata = pd.read_csv(fpath,skiprows=2)
    
    # remove nan type rows, standard transfers, rent, (Internet now included in venmo)
    toDrop = np.array([])
    for row in range(rdata.shape[0]):
        if type(rdata.Type[row]) != str:
            toDrop = np.append(toDrop,row)
        elif rdata.Type[row] == 'Standard Transfer':
            toDrop = np.append(toDrop,row)
            
    rdata = rdata.drop(toDrop)

    tmp = pd.to_datetime(rdata["Datetime"])
    tmp = tmp.dt.strftime('%b-%y')
    if tmp.iloc[0] != month:
        return 0

def getVenmoData(fpath,month):
    rdata = pd.read_csv(fpath,skiprows=2)
    
    # remove nan type rows, standard transfers, rent, (Internet now included in venmo)
    toDrop = np.array([])
    for row in range(rdata.shape[0]):
        if type(rdata.Type[row]) != str:
            toDrop = np.append(toDrop,row)
        elif rdata.Type[row] == 'Standard Transfer':
            toDrop = np.append(toDrop,row)
            
    rdata = rdata.drop(toDrop)

    tmp = pd.to_datetime(rdata["Datetime"])
    tmp = tmp.dt.strftime('%b-%y')
    if tmp.iloc[0] != month:
        return None
    
    # Move over the data we're interested in
    outData = pd.DataFrame(columns=["Account","Description","Date","Cost"])
    outData["Description"] = rdata["Note"]

    dates = pd.to_datetime(rdata["Datetime"])
    outData["Date"] = dates.dt.strftime('%Y-%m-%d')

    outData["Cost"] = rdata["Amount (total)"]

    return outData

def getRentVenmo(fpath):
    landlord = 'Wafa El Awar'

    rdata = pd.read_csv(fpath,skiprows=2)
    # remove nan type rows, standard transfers, rent, (Internet now included in venmo)
    for row in range(rdata.shape[0]):   
        if rdata.To[row] == landlord:
            entry = rdata["Amount (total)"].iloc[row]
            val = pd.to_numeric(entry.replace('$','').replace(' ','').replace(',',''))
            return val