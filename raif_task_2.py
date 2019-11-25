# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 05:08:11 2019

@author: Иван
"""

import pandas as pd
import numpy as np
from scipy import stats 


data = pd.read_csv('/usr/local/data/transactions.txt', sep = ',', header = None)

data.rename(columns= {0:'id',1: 'client',2:'transactions',3:'sector'}, inplace =True)
 
count_client = data.groupby(['client','sector']).sum().index.to_frame()
print("Количество клиентов совершивших транзакции в сегменте R : %d" 
      % len(count_client[count_client['sector'] == 'R']))

print("Количество клиентов совершивших транзакции в сегменте AF : %d" 
      % len(count_client[count_client['sector'] == 'AF']))

mean_transaction = data.groupby(['sector']).mean()['transactions']

print("Средний объем транзакции в секторе R : %.3f" % mean_transaction['R'])
print("Средний объем транзакции в секторе AF : %.3f" % mean_transaction['AF'])

def dover(segment,p):
    sigma = stats.norm.ppf(1-(1-p)/2) # Коэффицент  доверия
#    print(sigma)
     
    data_R = data[data['sector']== segment]
    X_mean = data_R['transactions'].mean()

    std = np.sqrt(np.sum((data_R['transactions']-X_mean)**2)/len(data_R))
#    print(std )
#    print(np.std(data_R['transactions']))
    se = std/(np.sqrt(len(data_R)))

    transaction_90_max = X_mean+se*sigma
    transaction_90_min = X_mean-se*sigma

    print("Доверительный интервал для сегмента %s : от %.2f до %.2f" %(segment,transaction_90_min,transaction_90_max))

def student():
    data_R = data[data['sector']== 'R']
    data_AF = data[data['sector'] == 'AF']
    
    X_mean_R = data_R['transactions'].mean()
    X_mean_AF = data_AF['transactions'].mean()
    
    sd_R = np.std(data_R['transactions'])
    sd_AF = np.std(data_AF['transactions'])
    
    t = abs(X_mean_AF-X_mean_R)/np.sqrt(((sd_R**2)/len(data_R))+((sd_AF**2)/len(data_AF)))
#    print(t)
    df = len(data_R)+len(data_AF)-2
    
    return stats.t.cdf(-t,df)*2
p = student()


if p < 0.1:
    print("Полученый уровень значимость равен %.3f это позволяет нам отклонить нулевую гипотезу" % p )
else :
    print("Полученый уровень значимость равен %.3f это не позволяет нам отклонить нулевую гипотезу" % p )
    
    