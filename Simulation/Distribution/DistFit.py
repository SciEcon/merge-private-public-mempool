import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
import random

# A class to fit distribution to Ethereum transaction attributes, which are Gas Limit, Used Gas, Gas Price as well as CPU Time

class DistFit():

    txGas = None
    txGasPrice = None
    utlization = None
    x = 0
    
    df2 = pd.read_csv('/Users/tianyuwu/Downloads/Transaction-Latency-main/Distribution/tx_data.csv')
    
    def fit():

        txUsedGas2 = np.log(DistFit.df2['receipt_gas_used']).values.reshape(-1,1)
        txPrice = np.log(DistFit.df2['gas_price']+0.001).values.reshape(-1,1)
        DistFit.txGas, DistFit.txGasPrice = DistFit.creation_fit(txUsedGas2,txPrice)


    def creation_fit(df,df1):
        K = 5
        g = GaussianMixture(n_components = K)
        gmm = g.fit(df)
        
        eps = 0.001
        K = 65
        gg = GaussianMixture(n_components = K)
        ggmm = gg.fit(df1)

        return gmm, ggmm


    def sample_transactions(n):
        gastx = DistFit.txGas.sample(n)[0]
        gastx = np.exp(gastx).flatten().round()
        gastx[gastx < 21000] = 21000
        gastx[gastx > 30000000] = 30000000

        gasprice = DistFit.txGasPrice.sample(n)[0]
        gasprice = np.exp(gasprice).flatten().round()

        UT = random.uniform(0,100)


        if (UT <= 6.57):
            utlization = 0
        elif (UT <= 27.07):
            utlization = random.uniform(0.1,20)
        elif (UT <= 34.75):
            utlization = random.uniform(20.1,40)
        elif (UT <= 40.34):
            utlization = random.uniform(40.1,60)
        elif (UT <= 44.97):
            utlization = random.uniform(60.1,80)
        elif (UT <= 48.91):
            utlization = random.uniform(80.1,95)
        elif (UT <= 100):
            utlization = random.uniform(95.1,100)     

        return gastx, gasprice, utlization
