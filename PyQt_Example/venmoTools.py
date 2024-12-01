# 
# Author: Nate Winneg
# Date: 2023-02-04
#
# Function functions to parse venmo data files
import numpy as np
import pandas as pd

basePath = 'C:/Users/nwinn/Desktop/Budget/data/'

def venmoCompute(year,month,landlord):
    # landlord = 'Wafa El Awar'
    vfile = basePath+year+'/'+month+'/Venmo_'+month.lower()+year[2:len(year)]+'.csv'
    rdata = pd.read_csv(vfile,skiprows=2)

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

def venmoData(year,month,landlord):
    vfile = basePath+year+'/'+month+'/Venmo_'+month.lower()+year[2:len(year)]+'.csv'
    rdata = pd.read_csv(vfile,skiprows=2)
    
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

def venmoRawData(year,month,landlord):
    vfile = basePath+year+'/'+month+'/Venmo_'+month.lower()+year[2:len(year)]+'.csv'
    rdata = pd.read_csv(vfile,skiprows=2)

    return rdata