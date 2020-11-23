import random
import requests
from threading import Thread, Event
import time

import numpy as np

from config import *


def random_parameter_combination(num_parameters):
    arr = []
    for i in range(num_parameters):
        _parameter = random.uniform(0, 1)
        arr.append(_parameter)
    return arr


def request_connect_peer(ip, port, peer_port):
    headers = {
        'cache-control': 'no-cache',
        'content-type': 'application/json'
    }
    data = '{\n    "Address": "' + peer_port + '"\n}'
    response = requests.post('http://{}:{}/connecttopeer'.format(ip, port), headers=headers, data=data)


def create_network_connections(nodes_information):
    '''
    Create connection among nodes on network
    '''
    print(nodes_information)
    nodes_connections = []
    list_connection = [nodes_information[0]]
    for i in range(1, len(nodes_information), 1):
        for j in range(len(list_connection)):
            connect_value = random.choice(range(2))
            if connect_value == 1:
                print('[x] Connect {} to {}'.format(nodes_information[i]['api_port'], 
                                                    list_connection[j]['api_port']))
                print('-------------')
                ip = 'localhost'
                port = nodes_information[j]['api_port']

                peer_port = '{}:{}'.format(nodes_information[i]['hostname'], 8000)
                action_thread = Thread(target=request_connect_peer(ip, port, peer_port))
                action_thread.start()
                action_thread.join(timeout=5)
                list_connection.append(nodes_information[i])
                continue


def request_send_coin(ip, port, from_address, to_address, amount):
    headers = {
        'cache-control': 'no-cache',
        'content-type': 'application/json'
    }

    data = '{\n    "From": "' + from_address + '",\n    "To": "' + to_address + '",\n    "Amount": ' + str(amount) + '\n}'

    response = requests.post('http://{}:{}/send'.format(ip, port), headers=headers, data=data)
    return response


def simulation_transaction(nodes_information, initiate_address_account, num_transaction_per_block):
    '''
    simulation send coin from address, nodes on network
    '''
    addresses_send_transaction_in_block = random.choices(initiate_address_account, k=num_transaction_per_block*2)
    print(len(addresses_send_transaction_in_block))
    for _block_idx in range(10):
        for i in range(num_transaction_per_block):
            ip = 'localhost'
            port = 8080
            from_address = addresses_send_transaction_in_block[i * 2]
            to_address = addresses_send_transaction_in_block[i * 2 + 1]
            amount = random.choice(range(5))
            send_coin_response = request_send_coin(ip, port, from_address, to_address, amount)
            print(send_coin_response.status_code)


def choose_sub_list_from_list(list, num_element):
    if num_element > len(list):
        print('[ERROR] num_element larger than length of list')
        return 
    results = []
    for i in range(num_element):
        check = True
        while check:
            _result = random.choice(list)
            if _result not in results:
                results.append(_result)
                check = False
    return results


def find_max_vote_in_current_candidate(peer_list, random_leader_idx):
    leader = random_leader_idx[0]
    for i in range(1, len(random_leader_idx), 1):
        if peer_list[random_leader_idx[i]].current_voted > peer_list[leader].current_voted:
            leader = random_leader_idx[i]
    return leader


def select_top_n_value_in_list(value_list, n):
    results = sorted(range(len(value_list)), key=lambda i: value_list[i], reverse=True)[:n]
    return results


def multiply_list_vs_list(list1, list2):
    arr_1 = np.array(list1)
    arr_2 = np.array(list2)
    return np.dot(arr_1, np.transpose(arr_2))


if __name__ == "__main__":
    parameters = random_parameter_combination(11)
    print(parameters)
