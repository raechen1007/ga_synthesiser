#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 06:30:27 2019

@author: RaeChen
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import chain
import numpy as np

def categories_counting(data):
    '''
        This function lists categories from all varaibles of a data. It is used to test 
        if individual has the same categories in each variables as the real data.
    '''
    unique, shape=[], []
    for i in range(data.shape[0]):
        unique.append(list(np.unique(data[i])))
        shape.append(len(list(np.unique(data[i]))))
    numeric=[]
    for level in shape:
        numeric.append(list(range(level)))
    return unique, numeric

def change_to_numeric(data):
    '''
        The function change data whose categories are in string format to numeric
    '''
    m,n=data.shape
    cat_list, num_list=categories_counting(data)
    cat_list=list(chain.from_iterable(cat_list))
    num_list=list(chain.from_iterable(num_list))
    trans=dict(zip(cat_list, num_list))
    num_data=np.zeros(data.shape, dtype='int64')
    for i in range(m):
        for j in range(n):
            num_data[i][j]=int(trans[data[i][j]])
    return num_data

def refine(data):
    '''
        Refine numeric data to 0-based level
    '''
    for row in data:
        if not min(row)==0:
            gap=min(row)
            n=data.shape[1]
            for i in range(n):
                row[i]=row[i]-gap
    return data


def restructure(data, target_index):
    '''
        restructure data to Keys+Target format 
    '''
    new=data.copy()
    new[target_index], new[-1]=new[-1], new[target_index].copy()
    return new
