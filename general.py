# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 09:39:23 2018

@author: yingr
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from random import sample
import pandas as pd
import numpy as np
import cookbook

def slices(n): 
    indices = range(n+1)
    while True:
        a, b = sorted(sample(indices, 2))
        yield slice(a, b)
        
def reverse_slices(n): #For round-CPC only
    '''
    The function creates a random block of an array
    '''
    indices = range(n+1)
    while True:
        a, b = sorted(sample(indices, 2))
        yield slice(0, a) 
        yield slice(b, n+1)
        
def psi_trans(fit_val,psi=1.0):
    N=len(fit_val)
    fit_trans=[0]*N
    for i in range(N):
        if fit_val[i]>=psi:
            fit_trans[i]=0.0
        else:
            fit_trans[i]=psi-fit_val[i]
    return fit_trans


def get_data(data_file, target_index):
    '''
        Getting original data from .cvs file
        Desired format of data: numeric array, 0-based indexed categories,
        in the format of key variables+target variable
    '''
    testdata=pd.read_csv(data_file)
    data=np.array(testdata).T
    ori_data=cookbook.restructure(data, target_index)
    m=data.shape[1]
    return ori_data, m

#def unique(data): 
#    unique=[]
#    for i in range(data.shape[0]):
#        unique.append(len(list(np.unique(data[i]))))
#    return tuple(unique)

def unique(data): #get the shape of data
    unique=[]
    for i in range(data.shape[0]):
        unique.append(max(data[i])-min(data[i])+1)
    return tuple(unique)
   
def create_array(data, shape): #Written by DS: duncan.g.smith@manchester.ac.uk
    '''
        Function to create full contingency table
    '''
    arr = np.zeros(shape)
    for case in data.T:
        arr[tuple(case)] += 1
    return arr
   
def JS_distance(P, Q):#Written by DS: duncan.g.smith@manchester.ac.uk
   mean = 0.5*P + 0.5*Q
   JS_divergence=((- mean * np.where(mean > 0, np.log2(mean), 0)).sum() -
           0.5 * (- P * np.where(P > 0, np.log2(P), 0)).sum() -
           0.5 * (- Q * np.where(Q > 0, np.log2(Q), 0)).sum())
   return JS_divergence ** 0.5

def uniqueness_indicator(data, full_table):
    indicator=[]
    for case in data.T:
        if full_table[tuple(case)]==1.0:
            indicator.append(tuple(case))
    return indicator
