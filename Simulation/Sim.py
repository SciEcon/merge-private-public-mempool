from Distribution.DistFit import DistFit
import numpy as np
import pandas as pd
import operator
import random
from statistics import mean, median, stdev 

class Sim(object):
        block_interval = 12.0  # Average block generation time after the Merge.
        gas_limit = 30000000
        sigma = 2000 # Arrival rate for transactions 
        Butilization = 1 # The block utilization level (it ranges from 0.0 to 1.0), where 0.0 indicates empty blocks and 1.0 indicates all blocks are full
        timer = 0 # It indicates the current simulation time, where 0 indicates the simulator has not yet started
        rounds = 3 # Number of simulation rounds

        mempool = [] 
        transactionsPool = []
        blockchain = [] 

class Transaction(object):
    def __init__(self,
	 id = random.randrange(100000000000), # the unique id or equivalently, the hash 
	 timestamp = 0, # the time when the transaction is created
	 sender = 0, # sender id
         to = 0, # receiver id
         value = 0, # amount of crypto in each tx
	 size = 0.000546, # tx size in MB
         gasLimit = 30000000,
         gasUsed = 0,
         gasPrice = 0,
         fee = 0,
         inclusion_time = 0,
         latency = 0):

        self.id = id
        self.timestamp = timestamp
        self.sender = sender
        self.to = to
        self.value = value
        self.size = size
        self.gasLimit = gasLimit
        self.gasUsed = gasUsed
        self.gasPrice = gasPrice
        self.fee = gasUsed * gasPrice
        self.inclusion_time = inclusion_time
        self.latency = inclusion_time - timestamp



class FullTransaction():
    counter = 0 # counter for tx created per second
    

    def create_transactions():
        j = 1
        Psize = 100 * Sim.sigma 

        gasUsed, gasPrice,_ = DistFit.sample_transactions(Psize)

        for i in range(Psize):
            FullTransaction.counter = FullTransaction.counter + 1 
            if FullTransaction.counter > Sim.sigma:
            	j = j + 1 
            	FullTransaction.counter = 0

            tx = Transaction()
            tx.id = random.randrange(100000000000)
            tx.timestamp = j
            tx.gasUsed = gasUsed[i]
            tx.gasPrice = gasPrice[i] / 1000000000
            tx.fee = tx.gasUsed * tx.gasPrice
            Sim.transactionsPool.append(tx)


    def execute_transactions():
        Sim.timer = Sim.timer + random.expovariate(1 / Sim.block_interval) 
        currentTime = Sim.timer 
        Sim.transactionsPool.sort(key=operator.attrgetter('gasPrice'), reverse=True)

        while len(Sim.transactionsPool) > 0:
            blocklimit = (Sim.gas_limit * Sim.Butilization)
            tx_x = 0
            for i in range (len(Sim.transactionsPool)):
                    if Sim.transactionsPool[i].timestamp <= currentTime:
                         tx_x += 1
            
            Sim.mempool += [tx_x]
            block = Block()
            block.depth = len(Sim.blockchain)
            block.timestamp = currentTime
            limit = 0 # calculate the total block gas limit
            count = 0

            while count < len(Sim.transactionsPool):

                    if  (blocklimit >= Sim.transactionsPool[count].gasUsed and Sim.transactionsPool[count].timestamp <= currentTime):
                            blocklimit -= Sim.transactionsPool[count].gasUsed
                            Sim.transactionsPool[count].inclusion_time = currentTime
                            Sim.transactionsPool[count].latency = Sim.transactionsPool[count].inclusion_time - Sim.transactionsPool[count].timestamp
                            block.transactions += [Sim.transactionsPool[count]]
                            limit += Sim.transactionsPool[count].gasUsed
                            del Sim.transactionsPool[count]
                            count = count - 1 
                    count += 1

            block.gasUsed = limit


            Sim.blockchain.append(block)
            currentTime += Sim.block_interval 


class Block():

    def __init__(self,
	 depth = 0,
	 id = 0,
	 previous = -1,
	 timestamp = 0,
	 miner = None,
	 transactions = [],
	 size = 1.0,
	 uncles = [],
         gaslimit = 30000000,
         gasUsed = 0):

        self.depth = depth
        self.id = id
        self.previous = previous
        self.timestamp = timestamp
        self.miner = miner
        self.transactions = transactions or []
        self.size = size
        self.uncles = uncles
        self.gaslimit = gaslimit
        self.gasUsed = gasUsed



def main():
    DistFit.fit() 
    latency = [[0 for x in range(5)] for y in range(Sim.rounds)] 

    for i in range(Sim.rounds):
            FullTransaction.create_transactions() 
            FullTransaction.execute_transactions()

            txList = []
            blocks = [[0 for x in range(5)] for y in range(len(Sim.blockchain))] 
            late = []

            for k in Sim.blockchain:
                    for j in range (len(k.transactions)):
                        txList.append(k.transactions[j])
                        late.append(k.transactions[j].latency)
                
            latency[i][0] = min(late)
            latency[i][1] = max(late)
            latency[i][2] = mean(late)
            latency[i][3] = median(late)
            latency[i][4] = stdev(late)
            
            transactionsList = [[0 for x in range(7)] for y in range(len(txList))]
            for i in range (len(txList)):
                    transactionsList[i][0] = txList[i].id
                    transactionsList[i][1] = txList[i].timestamp
                    transactionsList[i][2] = txList[i].gasUsed
                    transactionsList[i][3] = txList[i].gasPrice
                    transactionsList[i][4] = txList[i].fee
                    transactionsList[i][5] = txList[i].inclusion_time
                    transactionsList[i][6] = txList[i].latency

            for i in range (len(Sim.blockchain)):
                    blocks[i][0] = Sim.blockchain[i].depth
                    blocks[i][1] = Sim.blockchain[i].timestamp
                    blocks[i][2] = Sim.blockchain[i].gaslimit
                    blocks[i][3] = Sim.blockchain[i].gasUsed
                    blocks[i][4] = len(Sim.blockchain[i].transactions)

            Sim.blockchain = []
            Sim.transactionsPool = []
            Sim.timer = 0

    df = pd.DataFrame(transactionsList)
    df.columns = ['ID','Timestamp', 'Used Gas','Gas Price', 'Fee','Inclusion Time','Latency']
    df1 = pd.DataFrame(Sim.mempool)
    df2 = pd.DataFrame(blocks)
    df2.columns = ['ID','Timestamp', 'Gas Limit','Used Gas', '# of tx']
    df3 = pd.DataFrame(latency)
    df3.columns = ['Min','Max', 'Mean','Median', 'SD']

    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Transactions')
    df1.to_excel(writer, sheet_name='Network_Pending')
    df2.to_excel(writer, sheet_name='Blocks')
    df3.to_excel(writer,sheet_name='Latency')
    writer.save()


if __name__ == '__main__':
        main()
