# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 16:21:26 2018

@author: yingr
"""
import numpy as np
import copy
import individual
import population


'''
---------------------------------GA process------------------------------------
'''
def adaptive_pc(fitness, parameter):
    pc=parameter*fitness
    if pc>1.0:
        pc=1.0
    return pc

def adaptive_pm(pop_fit, parameter):
    '''
    F_pm(fitness) function for adaptive GA mutation operator
    F_pm(fitness)=mean(fitness)*k
    
    '''
    f_bar=np.mean(pop_fit)
    pm=parameter*f_bar
    if pm>1.0:
        pm=1.0
        
    pm_ls=[pm]*len(pop_fit)
    return pm_ls


def selection(Population, selection_fn, if_multi, *arg):
    if if_multi==False:
        selection=selection_fn(Population.pop_fitsca, *arg)
        pool=[]
        for i in selection:
            pool.append(copy.deepcopy(Population.candidates[i]))
        return pool
    else:
        selection=selection_fn(Population.pop_fitvar, *arg)
        pool=[]
        for i in selection:
            pool.append(copy.deepcopy(Population.candidates[i]))
        return pool
    #pool=list of individual classes

def crossover(pool, adaptive_pc, crossover_fn, pc, *arg): 
    size=len(pool)
    even=list(range(0,size-1,2))
    offspring=[]
    
    if adaptive_pc==False:
        for j in even:
            for _ in range(2):
                offspring.append(crossover_fn(pool[j].syn_data, 
                                              pool[j+1].syn_data, pc, *arg)[_])
                                                #pc or puc
        return offspring
    
    else:
        for j in even:
            for _ in range(2):
                pc=adaptive_pc(*arg)
                offspring.append(crossover_fn(pool[j].syn_data, 
                                              pool[j+1].syn_data, pc, *arg)[_])
                                                #pc or puc
        return offspring
    #offspring is a list of arrays that represent syn_data of offspring
    

def mutation(offspring, adaptive_pm, mutation_fn, pm, *arg):
    size=len(offspring)
    
    if adaptive_pm==False:
        for k in range(size):
            offspring[k]=mutation_fn(offspring[k],pm)
            
    else:
        for k in range(size):
            pm=adaptive_pm(*arg)
            offspring[k]=mutation_fn(offspring[k],pm)
            
    return offspring
    #offspring is a list of arrays that represent syn_data of offspring
    
def newPopulation(offspring, ori_data, m, shape, ori_full_table, obj, weight,
                   size):
    candidates=[]
    for syn_data in offspring:
        candidates.append(individual.Individual(syn_data, ori_data, m, shape, 
                                         ori_full_table, obj, weight))
    
    new_population=population.Population(ori_data, size, candidates)
    new_population.populationFitness()
    return new_population






        
    
    
    
    
    
    
