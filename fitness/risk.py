# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import general 
from itertools import product
import numpy as np

def dcapUnique(ori_data, syn_data, ori_full_table, syn_full_table):
    '''
        unique keys from original data
    '''
    count=np.unique(ori_data[:-1].T, return_counts=True, axis=0)
    unique_ori_key=[]
    for i in range(len(count[1])):
        if count[1][i]==1:
            unique_ori_key.append(count[0][i])
    
    '''
    unique key that has unique target in the original data, aka reference table     
    '''
    unique_ori_target=[]
    for key in unique_ori_key:
        unique_ori_target.append(np.where(ori_full_table[tuple(key)]==1)[0][0])
    reference_table=np.column_stack((np.array(unique_ori_key), np.array(unique_ori_target)))
    '''
        finding frequencies of key values appeared in reference table and also 
        in synthetic data
    '''
    corr_syn_key=[]
    for key in unique_ori_key:
        corr_syn_key.append(sum(syn_full_table[tuple(key)]))
    '''
        Finding frequencies of key+target values appeared in reference table and 
        also in synthetic data
    '''
    corr_syn_target=[] 
    for value in reference_table:
        corr_syn_target.append(syn_full_table[tuple(value)])
        
    paa=np.array([corr_syn_target[i]/corr_syn_key[i] for i in range(len(corr_syn_key))])
    paa[np.isnan(paa)]=0 #recode nan to 0
    
    dcap=np.mean(paa)
    return dcap

def dcap(ori_data, syn_data, m, shape, ori_full_table):
    '''
        Find uniques in synthetic data
    '''
    count=np.unique(syn_data.T, return_counts=True, axis=0)
    unique_data=[]
    for i in range(len(count[1])):
        if count[1][i]==1:
            unique_data.append(count[0][i])
    unique_data=np.array(unique_data).T
    
    '''
        cap table
    '''
    target=ori_data[-1] #default ori_data[-1] is target variable
    prop=np.unique(target, return_counts=True)[1]/m #frequencies
    
    baseline_cap=[]
    for value in target:
        baseline_cap.append(prop[value])
        
    baseline_cap=np.array(baseline_cap)
    
    shape_key=shape[:-1] #shape of key variables (equivalence class)
    
    ori_key=ori_data[:-1] #extract key vars from ori_data
    syn_key=syn_data[:-1] #extract key vars from syn_data
    
    ori_key_table=general.create_array(ori_key, shape_key) #getting full CT of key vars from ori_data
    syn_key_table=general.create_array(syn_key, shape_key) #getting full CT of key vars from syn_data
    
    syn_full_table=general.create_array(syn_data, shape)#getting full CT of all vars from syn_data
    
    ori_cap, syn_cap=np.zeros(m), np.zeros(m)
    for i in range(m):
        ori_cap[i]=ori_full_table[tuple(ori_data.T[i])]/ori_key_table[tuple(ori_key.T[i])]
        syn_cap[i]=syn_full_table[tuple(ori_data.T[i])]/syn_key_table[tuple(ori_key.T[i])]
        
    cap_table=np.vstack((ori_data, ori_cap, syn_cap, baseline_cap))
    
    '''
        dcap
    '''
    dcap=(np.mean(cap_table[-2])-np.mean(cap_table[-1]))/(np.mean(cap_table[-3])-np.mean(cap_table[-1]))
    return dcap

def rcap(ori_data, syn_data, m, shape, ori_full_table):
    syn_full_table=general.create_array(syn_data, shape)#getting full CT of all vars from syn_data
    shape_key=shape[:-1]
    
    itr=[]
    for number in shape_key:
        itr.append(list(range(number))) 
    unv_keys=list(product(*itr))
    
    ori_tar, syn_tar=[], []#freqencies of target values for all set of keys in ori/syn_data
    for key in unv_keys:
        ori_tar.append(ori_full_table[key])
        syn_tar.append(syn_full_table[key])
    
    location=[[],[]] #location lists
    for j in range(len(unv_keys)):
        if np.count_nonzero(syn_tar[j])==1: #given conditions of cap(syn)=1
            location[0].append(j) #location of which set of key has cap(syn)=1
            location[1].append(list(np.nonzero(syn_tar[j])[0])[0]) 
            #location of the problematic target value 
            '''
            we know that when cap(syn)=1 the set of key only has one target value
            appears in synthetic data. See proof above.
            '''
    
    sum1, sum2=0, 0
    '''
    sum1: cumulate all number of cases from problematic set of keys
    sum1: cumulate all number of cases from problematic target value of
          the corresponding set of keys.
    '''
    for loc in range(len(location[0])):
        where_key, where_tar=location[0][loc], location[1][loc]
        sum1+=sum(ori_tar[where_key])
        sum2+=ori_tar[where_key][where_tar]
    
    if sum1!=0:
        return sum2/sum1
    else:
        return 0