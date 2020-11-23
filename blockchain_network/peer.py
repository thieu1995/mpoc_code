import random

from includes.utils import *
from blockchain_network.wallet import Wallet


class PeerDPoS:

    def __init__(self, current_voted=0, number_leader_time=0, connected_peers=None):
        self.current_voted = 0  # Current voted from the other peers
        self.number_leader_time = 0  # number of time to become leader
        self.risk_accept = random.uniform(0, 1)
        self.connected_peers = connected_peers
        self.rate_reward_for_voter = random.choice([0.3, 0.4, 0.5, 0.6, 0.7])
        self.voted_information = []
        self.vote_for_information = []
        self.init_wallets()

    def init_wallets(self):
        # Initiate connected wallet
        self.connected_wallets = []
        self.number_connected_wallet = random.choice(range(10, 100))
        for i in range(self.number_connected_wallet):
            _address = 'add_{}'.format(i)
            _balance = random.uniform(10, 100)
            _stake_value = 0
            _wallet = Wallet(_address, _balance, _stake_value)
            self.connected_wallets.append(_wallet)

        # Initiate mine wallet
        mine_address = 'mine_add_{}'.format(i)
        mine_balance = random.uniform(10, 100)
        mine_stake_value = 1
        self.mine_wallet = Wallet(mine_address, mine_balance, mine_stake_value)


class PeerMDPoS:

    def __init__(self, current_voted=0, number_leader_time=0, connected_peers=None):
        self.number_leader_time = 0  # number of time to become leader
        self.connected_peers = connected_peers
        self.rate_reward_for_voter = random.choice([0.1, 0.2, 0.3, 0.4, 0.5])
        self.risk_accept = random.uniform(0, 1)
        self.famous_prob = random.uniform(0, 1)
        self.voted_information = []  # voted information from other peers
        self.vote_for_information = []  # vote information for other peers
        self.total_transaction_in_produced_block = 0

        self.init_wallets()
        # List of feature
        self.transaction = []  # Number of transaction go out from this peer
        self.current_voted = 0  # Current voted from the other peers
        self.staked_value = 0  # stake value locked to vote
        self.number_true_vote = 0  # The number of correct leader votes
        self.number_leader_time = 0  # The number of times to become leader
        self.number_address_connect_to = 0  # Number of address connect to this peer
        self.number_epoch_join_in_network = 0  # The number of epochs this peer join in network
    
    def create_new_wallet(self, n):
        for i in range(n):
            _address = 'add_{}'.format(len(self.connected_wallets) + i)
            _balance = random.uniform(100, 1000)
            _stake_value = 0
            _wallet = Wallet(_address, _balance, _stake_value)
            self.connected_wallets.append(_wallet)

    def init_wallets(self):
        # Initiate connected wallet
        self.connected_wallets = []
        self.number_connected_wallet = random.choice(range(10, 100))
        for i in range(self.number_connected_wallet):
            _address = 'add_{}'.format(i)
            _balance = random.uniform(100, 1000)
            _stake_value = 0
            _wallet = Wallet(_address, _balance, _stake_value)
            self.connected_wallets.append(_wallet)

        # Initiate mine wallet
        mine_address = 'mine_add_{}'.format(i)
        mine_balance = random.uniform(100, 1000)
        mine_stake_value = 0
        self.mine_wallet = Wallet(mine_address, mine_balance, mine_stake_value)


