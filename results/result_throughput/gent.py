nodes = [200, 300]
n_value = [75, 100, 125]
k_value = [18, 21, 24]
for _node in nodes:
    for _n_value in n_value:
        for _k_value in k_value:
            file_name = './mpoc/{}_{}_{}.txt'.format(_node, _n_value, _k_value)
            f = open(file_name, 'r')
            arr = []
            for line in f:
                if line == 'l1:\n' or line == 'l2:\n' or line == 'l3:\n' or line == 'l4:\n' or line == 'l5:\n' or line == '\n':
                    continue
                num_transaction = int(line.split(" ")[3])
                arr.append(num_transaction)
            avg = sum(arr) / len(arr)
            max_arr = max(arr)
            print("{} node, n = {}, k = {} ====> avg: {}, max: {}".format(_node, _n_value, _k_value, round(avg, 2), max_arr))

print('==========')

nodes = [200, 300]
k_value = [18, 21, 24]
for _node in nodes:
    for _k_value in k_value:
        arr = []
        file_name = './dpos/{}_{}.txt'.format(_node, _k_value)
        f = open(file_name, 'r')
        for line in f:
            if line == 'l1:\n' or line == 'l2:\n' or line == 'l3:\n' or line == 'l4:\n' or line == 'l5:\n' or line == '\n':
                continue
            num_transaction = int(line.split(" ")[3])
            arr.append(num_transaction)
        avg = sum(arr) / len(arr)
        max_arr = max(arr)
        print("{} node, k={} ====> avg: {}, max: {}".format(_node, _k_value, round(avg, 2), max_arr))