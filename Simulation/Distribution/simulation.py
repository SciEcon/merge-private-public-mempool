import pandas as pd
import numpy as np
import random
from google.colab import drive
drive.mount('/content/drive')

class User:
    def __init__(self, gas_price):
        self.gas_price = gas_price

class Miner:
    def __init__(self, alpha, target):
        self.alpha = alpha
        self.target = target
        self.is_dark = target < alpha

    def choose_pool(self, mempool_fee, dark_fee):
        if self.is_dark:
            if dark_fee > mempool_fee:
                return "dark"
            else:
                return "mempool"
        else:
            if mempool_fee > dark_fee:
                return "mempool"
            else:
                return "dark"

class Arbitrager:
    def __init__(self, gamma):
        self.gamma = gamma

    def arbitrage(self, mempool_fee, dark_fee):
        profit = (mempool_fee - dark_fee) / dark_fee
        if profit > self.gamma:
            return True
        else:
            return False

# Set up the simulation parameters
num_users = 100
num_miners = 100
num_arbitragers = 2
alpha = 0.5
target = 0.1
gamma = 0.1
num_time_steps = 1000
mempool = []
dark_pool = []
mempool_users = []
dark_users = []

# Create the miners
miners = [Miner(alpha, target) for i in range(num_miners)]

df = pd.read_csv('/content/tx_data1.csv', index_col = 0)
gas_price = df['gas_price'][:num_users].tolist()

# Create the users
users = [User(gas_price[i]) for i in range(num_users)]

# Create the arbitrager
arbitragers = [Arbitrager(gamma) for i in range(num_arbitragers)]

# Initialize the fee variables
mempool_fee = 0
dark_fee = 0

# Loop over time steps
for t in range(num_time_steps):
    # Set the new fees
    mempool_fee = random.uniform(0, 100)
    dark_fee = random.uniform(0, 100)

    # Loop over the miners
    for miner in miners:
        # Choose the pool
        pool_choice = miner.choose_pool(mempool_fee, dark_fee)

        # If the miner chooses the mempool, add them to the mempool list
        if pool_choice == "mempool":
            mempool.append(miner)

        # If the miner chooses the dark pool, add them to the dark pool list
        elif pool_choice == "dark":
            dark_pool.append(miner)

    # Loop over the users
    for user in users:
        # Choose the pool with the lowest fee
        if mempool_fee < dark_fee:
            user_choice = "mempool"
        else:
            user_choice = "dark"

        # Add the user to the chosen pool
        if user_choice == "mempool":
            mempool_users.append(user)
        else:
            dark_users.append(user)

    # Loop over the arbitragers
    for arbitrager in arbitragers:
        # Check if there is a profitable arbitrage opportunity
        if arbitrager.arbitrage(mempool_fee, dark_fee):
            # If the mempool fee is higher, buy from the dark pool
            if mempool_fee > dark_fee:
                for user in dark_users:
                    if user.gas_price >= dark_fee:
                        user.gas_price = mempool_fee
            # If the dark fee is higher, buy from the mempool
            else:
                for user in mempool_users:
                    if user.gas_price >= mempool_fee:
                        user.gas_price = dark_fee
