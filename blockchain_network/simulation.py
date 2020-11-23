import random
import os
import requests
import json
import time
import subprocess
import statistics  

from includes.utils import *
from blockchain_network.peer import PeerDPoS, PeerMDPoS
from config import *


class Simulator:
    num_transaction_per_block = BlockchainNetworkConfig.NUM_TRANSACTION_PER_BLOCK
    initiate_node_information = BlockchainNetworkConfig.INITIATE_NODE_INFORMATION
    initiate_address = BlockchainNetworkConfig.INITIATE_ADDRESS
    reward_for_each_block = 10
    reward_for_each_transaction = 0.1

    def __init__(self, weights=None, num_round=None, num_peer_on_network=None, num_leader_each_round=None,
                 num_candidate_leader=None, num_peer_in_round_1=None, rate_peers_change_each_round=None):
        self.weights = weights
        self.num_round = num_round
        self.num_peer_on_network = num_peer_on_network
        self.num_leader_each_round = num_leader_each_round
        self.num_candidate_leader = num_candidate_leader
        self.num_peer_in_round_1 = num_peer_in_round_1
        self.rate_peers_change_each_round = rate_peers_change_each_round

    def leader_reward_for_voters(self, leader_idx):
        leader = self.peers_on_network[leader_idx]

        for _voted_information in leader.voted_information:
            self.peers_on_network[_voted_information[0]].mine_wallet.balance += \
                self.reward_for_each_block * _voted_information[1] * leader.rate_reward_for_voter / leader.current_voted
        return

    def first_execute_on_network(self):
        # First vote on network
        for _peer_idx in range(len(self.peers_on_network)):
            _peer = self.peers_on_network[_peer_idx]
            # set up transaction
            _peer.transaction.append(random.choice(range(1, int(self.num_peer_on_network / 10), 1)))

            # set up vote
            value_for_vote = []
            total_value_for_vote = 1
            for _idx in range(len(self.peers_on_network)):
                # List feature affect to vote decision:
                # # That peer connect to me or not
                if _idx in _peer.connected_peers:
                    _connected_value = 1 / 2
                else:
                    _connected_value = 0
                _value_for_vote = _connected_value
                total_value_for_vote += _value_for_vote
                value_for_vote.append(_value_for_vote)

            vote_for_peer_idx = select_top_n_value_in_list(value_for_vote, self.num_leader_each_round)
            vote_for_peer_value = 1
            for j in vote_for_peer_idx:
                vote_for_peer_value += value_for_vote[j]

            # TODO @thangbk2209 need change. It is randomly.
            _stake_value = random.uniform(0, _peer.mine_wallet.balance * vote_for_peer_value / total_value_for_vote)

            _peer.mine_wallet.lock_stake(_stake_value)
            for _vote_for_peer_idx in vote_for_peer_idx:
                _peer.vote_for_information.append([_vote_for_peer_idx, _stake_value])
                self.peers_on_network[_vote_for_peer_idx].current_voted += _stake_value
                self.peers_on_network[_vote_for_peer_idx].voted_information.append([_peer_idx, _stake_value])
            _peer.number_node_vote_for = len(_peer.vote_for_information)

    def change_vote_on_network(self, _round):
        num_not_satisfy = 0

        for _peer_idx in self.peers_idx_active_on_network:
            _peer = self.peers_on_network[_peer_idx]

            # Check this peer satisfy or not
            _balance_delta = _peer.mine_wallet.balance - _peer.mine_wallet.start_balance
            if _balance_delta <= 21 * _round * self.reward_for_each_block / len(self.peers_on_network):
                satisfy = False
            else:
                satisfy = True
            if satisfy == False:
                num_not_satisfy += 1
                if _peer.risk_accept <= 0.75:
                    _peer_vote_for_information = _peer.vote_for_information
                    _peer_idx_vote_for = [_peer_vote_for_information[i][0] for i in range(len(_peer_vote_for_information))]
                    remove_value = []
                    for i in range(len(_peer_idx_vote_for)):
                        if _peer_idx_vote_for[i] in self.leader_and_candidate_idx:
                            continue
                        else:
                            try:
                                self.peers_on_network[_peer_vote_for_information[i][0]].current_voted -= _peer.mine_wallet.stake_value
                                self.peers_on_network[_peer_vote_for_information[i][0]].voted_information.remove([_peer_idx, _peer.mine_wallet.stake_value])
                                remove_value.append(_peer_vote_for_information[i])
                            except AttributeError:
                                pass
                            
                            for j in range(len(self.leader_and_candidate_idx)):
                                if self.leader_and_candidate_idx[j] not in _peer_idx_vote_for \
                                    and len(_peer.vote_for_information) < self.num_leader_each_round:
                                    self.peers_on_network[_peer_idx].vote_for_information.append(
                                        [self.leader_and_candidate_idx[j], _peer.mine_wallet.stake_value])
                                    self.peers_on_network[self.leader_and_candidate_idx[j]].current_voted \
                                        += _peer.mine_wallet.stake_value
                                    self.peers_on_network[self.leader_and_candidate_idx[j]].voted_information.append(
                                        [_peer_idx, _peer.mine_wallet.stake_value])
                    for _remove_value in remove_value:
                        self.peers_on_network[_peer_idx].vote_for_information.remove(_remove_value)
                else:
                    remove_value = []
                    for i in range(len(_peer.vote_for_information)):
                        if _peer.vote_for_information[i][0] not in self.leader_and_candidate_idx:
                            remove_value.append(_peer.vote_for_information[i])
                            
                            self.peers_on_network[_peer.vote_for_information[i][0]].current_voted \
                                -= _peer.mine_wallet.stake_value
                            self.peers_on_network[_peer.vote_for_information[i][0]].voted_information.remove(
                                [_peer_idx, _peer.mine_wallet.stake_value])
                    for _remove_value in remove_value:
                        self.peers_on_network[_peer_idx].vote_for_information.remove(_remove_value)
                    _peer_vote_for_information = _peer.vote_for_information
                    _peer_idx_vote_for = [_peer_vote_for_information[i][0] for i in range(len(_peer_vote_for_information))]
                    _short = self.num_leader_each_round - len(_peer_idx_vote_for)

                    candidate = []
                    for i in self.leader_and_candidate_idx:
                        if i not in _peer_idx_vote_for:
                            candidate.append(i)
                    delegate = []
                    num_add = 0
                    need_to_add = self.num_leader_each_round + 1 - len(_peer.vote_for_information)
                    if need_to_add > 0:
                        for i in range(len(candidate)):
                            dice = random.uniform(0, 1)
                            if len(_peer.vote_for_information) + num_add <= self.num_leader_each_round:
                                if dice < (1 + num_add) / (1 + need_to_add):
                                    num_add += 1
                                    delegate.append(i)
                    for i in delegate:
                        _peer_idx_vote_for.append(i)
                        self.peers_on_network[_peer_idx].vote_for_information.append([i, _peer.mine_wallet.stake_value])
                        self.peers_on_network[i].current_voted += _peer.mine_wallet.stake_value
                        self.peers_on_network[i].voted_information.append([_peer_idx, _peer.mine_wallet.stake_value])

    def change_in_round(self, _round):
        # change transaction, vote, address, add new peer
        start_time = time.time()
        # Change vote of all on the network
        if _round > 2:
            try:
                self.change_vote_on_network(_round)
            except:
                pass

        # Add transaction of all peer on the network
        for _peer_idx in self.peers_idx_active_on_network:
            if _peer_idx in self.leader_and_candidate_idx and self.peers_on_network[_peer_idx].famous_prob > 0.9:
                self.peers_on_network[_peer_idx].transaction.append(random.choice(range(1, int(self.num_peer_on_network * 0.1), 1)))
            elif _peer_idx in self.leader_and_candidate_idx and self.peers_on_network[_peer_idx].famous_prob > 0.75:
                self.peers_on_network[_peer_idx].transaction.append(random.choice(range(1, int(self.num_peer_on_network * 0.08), 1)))
            elif _peer_idx in self.leader_and_candidate_idx and self.peers_on_network[_peer_idx].famous_prob > 0.5:
                self.peers_on_network[_peer_idx].transaction.append(random.choice(range(1, int(self.num_peer_on_network * 0.065), 1)))
            elif _peer_idx in self.leader_and_candidate_idx and self.peers_on_network[_peer_idx].famous_prob > 0.25:
                self.peers_on_network[_peer_idx].transaction.append(random.choice(range(1, int(self.num_peer_on_network * 0.055), 1)))
            else:
                self.peers_on_network[_peer_idx].transaction.append(random.choice(range(1, int(self.num_peer_on_network * 0.05), 1)))

        # Change number of nodes on the network
        num_current_peers_on_network = len(self.peers_idx_active_on_network)

        num_peers_change_in_that_round = random.choice(range(
            int(self.rate_peers_change_each_round * num_current_peers_on_network)))

        join_or_leave = random.choice(['join', 'leave'])
        if join_or_leave == 'join':
            for i in range(num_peers_change_in_that_round):
                # Create new peers
                _current_voted = 0
                _number_leader_time = 0
                num_connected_peers = random.choice(range(10, num_current_peers_on_network, 1))
                connected_peers = []
                _peer = PeerMDPoS(_current_voted, _number_leader_time, connected_peers)

                # Vote for other peers
                _stake_value = random.uniform(0, _peer.mine_wallet.balance / 10)
                _peer.mine_wallet.lock_stake(_stake_value)

                number_peer_vote_for = random.choice(range(10, self.num_leader_each_round, 1))
                vote_for_peer_idx = random.choices(self.leader_and_candidate_idx, k=number_peer_vote_for)
                for _vote_for_peer_idx in vote_for_peer_idx:
                    _peer.vote_for_information.append([_vote_for_peer_idx, _stake_value])
                    self.peers_on_network[_vote_for_peer_idx].current_voted += _stake_value
                    self.peers_on_network[_vote_for_peer_idx].voted_information.append([len(self.peers_on_network) + 1, _stake_value])
                _peer.number_node_vote_for = number_peer_vote_for
                _peer.transaction.append(0)
                self.peers_idx_active_on_network.append(len(self.peers_on_network))
                self.peers_on_network.append(_peer)
        else:
            # define peer leave from the network
            peer_not_in_round_1_candidate = []
            for _peer_idx in self.peers_idx_active_on_network:
                if _peer_idx not in self.peer_in_round_1_idx_and_candidates:
                    peer_not_in_round_1_candidate.append(_peer_idx)
            peer_leave_from_network = random.choices(peer_not_in_round_1_candidate, k=num_peers_change_in_that_round)
            for _peer_leave_from_network_idx in peer_leave_from_network:
                for _peer_leave_vote_for in self.peers_on_network[_peer_leave_from_network_idx].vote_for_information:
                    try:
                        self.peers_on_network[_peer_leave_vote_for[0]].current_voted -= _peer_leave_vote_for[1]
                        self.peers_on_network[_peer_leave_vote_for[0]].voted_information\
                            .remove([_peer_leave_from_network_idx, _peer_leave_vote_for[1]])
                    except:
                        pass
            try:
                for _peer_idx in peer_leave_from_network:
                    self.peers_on_network[_peer_idx] = None
                    self.peers_idx_active_on_network.remove(_peer_idx)
            except ValueError:
                pass

    def new_peer_connect_to_network(self):
        # randomly new node join in network
        num_new_node = random.choice(range(2))
        if num_new_node > 0:
            for i in range(num_new_node):
                _current_voted = 0
                _number_leader_time = 0
                num_connected_peers = random.choice(range(1, len(self.peers_on_network), 1))
                connected_peers = random.choices(range(len(self.peers_on_network)), k=num_connected_peers)
                for _peer_idx in connected_peers:
                    self.peers_on_network[_peer_idx].connected_peers.append(len(self.peers_on_network))
                if Config.CONSENSUS_METHOD == 'dpos':
                    _peer = PeerDPoS(_current_voted, _number_leader_time, connected_peers)
                elif Config.CONSENSUS_METHOD == 'mdpos':
                    _peer = PeerMDPoS(_current_voted, _number_leader_time, connected_peers)
                self.peers_on_network.append(_peer)

    def simulate_dpos(self, num_candidate_leader):
        print('[1] Start simulating delegated proof of stake algorithms')

        # Create peer list and connection among peers on network
        # # Initiate matrix connection between all peers
        connection_matrix = []
        for i in range(self.num_peer_on_network):       # 200
            _i_connect_information = []
            for j in range(i):
                _i_connect_information.append(connection_matrix[j][i])
            _i_connect_information.append(0)
            if i != self.num_peer_on_network - 1:
                for j in range(i+1, self.num_peer_on_network, 1):
                    _connect_decision = random.choice([0, 1])
                    _i_connect_information.append(_connect_decision)
                if 1 not in _i_connect_information:
                    random_peer_idx = random.choice(range(i+1, self.num_peer_on_network, 1))
                    _i_connect_information[random_peer_idx] = 1
            connection_matrix.append(_i_connect_information)

        # # Create peers and their connection base on matrix connection
        self.peers_on_network = []
        for peer_idx in range(self.num_peer_on_network):
            _current_voted = 0
            _number_leader_time = 0
            connected_peers = [i for i, e in enumerate(connection_matrix[peer_idx]) if e == 1]
            _peer = PeerDPoS(_current_voted, _number_leader_time, connected_peers)
            self.peers_on_network.append(_peer)

        for _round in range(self.num_round):
            print('--> Round {}: '.format(_round))
            # Should create some transactions to change balance of mine wallet
            if _round >= 2:
                start_time = time.time()

                self.change_vote_on_network(_round)

            _list_current_vote = []
            for _peer_idx in range(len(self.peers_on_network)):
                _list_current_vote.append(self.peers_on_network[_peer_idx].current_voted)
            leader_idx = select_top_n_value_in_list(_list_current_vote, self.num_leader_each_round)
            self.leader_and_candidate_idx = select_top_n_value_in_list(
                _list_current_vote, self.num_leader_each_round + self.num_candidate_leader)
            # Change rate reward here

            for _leader_idx in leader_idx:
                self.peers_on_network[_leader_idx].number_leader_time += 1
                self.peers_on_network[_leader_idx].mine_wallet.balance += \
                    self.reward_for_each_block * (1 - self.peers_on_network[_leader_idx].rate_reward_for_voter)
                # Reward for voter
                self.leader_reward_for_voters(_leader_idx)
        
        peers_number_leader_time = []
        for _peer_idx in range(len(self.peers_on_network)):
            peers_number_leader_time.append(self.peers_on_network[_peer_idx].number_leader_time)

        print('[COMPLETE] Simulate delegated proof of stake complete')

    def simulate_mdpos(self):
        # Create peer list and connection among peers on network
        # # Initiate matrix connection between all peers
        connection_matrix = []
        for i in range(self.num_peer_on_network):
            _i_connect_information = []
            for j in range(i):
                _i_connect_information.append(connection_matrix[j][i])
            _i_connect_information.append(0)
            if i != self.num_peer_on_network - 1:
                for j in range(i+1, self.num_peer_on_network, 1):
                    _connect_decision = random.choice([0, 1])
                    _i_connect_information.append(_connect_decision)
                if 1 not in _i_connect_information:
                    random_peer_idx = random.choice(range(i+1, self.num_peer_on_network, 1))
                    _i_connect_information[random_peer_idx] = 1
            connection_matrix.append(_i_connect_information)

        # # Create peers and their connection base on matrix connection
        num_famous_peer = 0
        self.peers_on_network = []
        self.peers_idx_active_on_network = []
        for peer_idx in range(self.num_peer_on_network):
            _current_voted = 0
            _number_leader_time = 0
            connected_peers = [i for i, e in enumerate(connection_matrix[peer_idx]) if e == 1]
            _peer = PeerMDPoS(_current_voted, _number_leader_time, connected_peers)
            self.peers_on_network.append(_peer)
            self.peers_idx_active_on_network.append(peer_idx)

        # # First execute on the network includes: Voting of all nodes.
        self.first_execute_on_network()

        self.total_transaction = 0
        for _round in range(self.num_round):
            start_time = time.time()
            self.round_total_transaction = 0

            # Changing in round
            if _round > 0:
                self.change_in_round(_round)

            # Choose top transaction ranking into round 1
            for _peer_idx in self.peers_idx_active_on_network:
                self.round_total_transaction += self.peers_on_network[_peer_idx].transaction[-1]
            self.total_transaction += self.round_total_transaction
            current_transaction_ranking_value = []
            for _peer_idx in self.peers_idx_active_on_network:
                if _round < 1:
                    transaction_rank_all = sum(self.peers_on_network[_peer_idx].transaction)
                    current_transaction_ranking_value.append(transaction_rank_all)
                else:
                    transaction_rank_all = sum(self.peers_on_network[_peer_idx].transaction)
                    transaction_rank_last_round = self.peers_on_network[_peer_idx].transaction[-1]
                    _current_transaction_ranking_value = \
                        (transaction_rank_all / self.total_transaction + transaction_rank_last_round / self.round_total_transaction) / 2
                    current_transaction_ranking_value.append(transaction_rank_all)
            _peer_in_round_1_idx = select_top_n_value_in_list(current_transaction_ranking_value, self.num_peer_in_round_1)
            peer_in_round_1_idx = []
            for _id in range(len(_peer_in_round_1_idx)):
                peer_in_round_1_idx.append(self.peers_idx_active_on_network[_peer_in_round_1_idx[_id]])
            round_1_candidates = select_top_n_value_in_list(
                current_transaction_ranking_value, self.num_peer_in_round_1 + self.num_candidate_leader)

            self.peer_in_round_1_idx_and_candidates = []
            for _id in range(len(round_1_candidates)):
                self.peer_in_round_1_idx_and_candidates.append(self.peers_idx_active_on_network[round_1_candidates[_id]])

            # Compute feature value of peer in round 1
            peer_feature = []
            for _peer_idx in peer_in_round_1_idx:
                _peer = self.peers_on_network[_peer_idx]
                if _round < 10:
                    _peer_feature = [sum(_peer.transaction), _peer.transaction[-1], sum(_peer.transaction), 
                                     _peer.current_voted, len(_peer.voted_information), _peer.mine_wallet.stake_value,
                                     len(_peer.vote_for_information), _peer.number_true_vote, _peer.number_leader_time,
                                     _peer.total_transaction_in_produced_block]
                else:
                    _peer_feature = [sum(_peer.transaction), _peer.transaction[-1], sum(_peer.transaction[-10:]), 
                                     _peer.current_voted, len(_peer.voted_information), _peer.mine_wallet.stake_value,
                                     len(_peer.vote_for_information), _peer.number_true_vote, _peer.number_leader_time,
                                     _peer.total_transaction_in_produced_block]
                peer_feature.append(_peer_feature)
            normalize_information = []
        
            for i in range(len(peer_feature[0])):
                _feature_i = []
                for j in range(len(peer_feature)):
                    _feature_i.append(peer_feature[j][i])

                _min_feature = min(_feature_i)
                _max_feature = max(_feature_i)
                if _max_feature == _min_feature:
                    _max_feature += 1
                normalize_information.append([_min_feature, _max_feature])
            _list_current_feature_value = []
            for _peer_feature in peer_feature:
                _normalize_peer_feature = []
                for i in range(len(_peer_feature)):
                    _normalize_peer_feature.append(
                        (_peer_feature[i] - normalize_information[i][0]) / \
                            (normalize_information[i][1] - normalize_information[i][0]))
                _peer_value = multiply_list_vs_list(self.weights, _normalize_peer_feature)
                _list_current_feature_value.append(_peer_value)

            # Choose leader and candidate nodes on the network base on top n+k criteria nodes on the network
            leader_candidate = select_top_n_value_in_list(
                _list_current_feature_value, self.num_leader_each_round + self.num_candidate_leader)
            self.leader_and_candidate_idx = []
            leader_idx = []
            for _id in range(len(leader_candidate)):
                if _id <= self.num_leader_each_round:
                    leader_idx.append(peer_in_round_1_idx[leader_candidate[_id]])
                self.leader_and_candidate_idx.append(peer_in_round_1_idx[leader_candidate[_id]])

            # update value
            try:
                for _leader_idx in leader_idx:
                    # update number leader time
                    self.peers_on_network[_leader_idx].number_leader_time += 1
                    self.peers_on_network[_leader_idx].total_transaction_in_produced_block += random.choice(range(50, 150))
                    # update number true vote

                    for _voted_information in self.peers_on_network[_leader_idx].voted_information:          
                            self.peers_on_network[_voted_information[0]].number_true_vote += 1
                    self.peers_on_network[_leader_idx].mine_wallet.balance += \
                        self.reward_for_each_block * (1 - self.peers_on_network[_leader_idx].rate_reward_for_voter)
                    # Reward for voter
                    self.leader_reward_for_voters(_leader_idx)
            except:
                pass
            # update number epoch
            for _peer_idx in self.peers_idx_active_on_network:
                self.peers_on_network[_peer_idx].number_epoch_join_in_network += 1
            
            end_time = time.time()
        peers_number_leader_time = []
        for _peer_idx in self.peers_idx_active_on_network:
            peers_number_leader_time.append(self.peers_on_network[_peer_idx].number_leader_time)
        leader_time = [_peers_number_leader_time for _peers_number_leader_time in peers_number_leader_time if _peers_number_leader_time != 0]
        _max_leader_time = max(peers_number_leader_time)
        peers_number_leader_time_normalize = []
        for i in range(len(peers_number_leader_time)):
            peers_number_leader_time_normalize.append(peers_number_leader_time[i] / _max_leader_time)
        fitness = statistics.variance(peers_number_leader_time_normalize)
        return fitness

    def compute_fitness_mdpos(self):
        peers_number_leader_time_normalize = self.simulate_mdpos()
        fitness = statistics.variance(peers_number_leader_time_normalize)
        return fitness
