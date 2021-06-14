#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 06:42:33 2019

@author: RaeChen
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import general

def full_divergence(syn_data, ori_data, m, shape, ori_full_table):
    P=ori_full_table/m
    Q=general.create_array(syn_data,shape)/m
    delta=general.JS_distance(P,Q)
    return delta