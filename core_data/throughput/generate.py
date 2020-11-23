nodes = [200, 300]
n_value = [75, 100, 125]
time = [1, 2, 3]
for _node in nodes:
    for _n_value in n_value:
        max = 0
        avg = 0
        for _time in time:
            file_name = '{}-{}-21-{}'.format(_node, _n_value, _time)
            f = open(file_name, 'r')
            sum = 0
            av = 0
            points=[]
            for line in f:
                av += 1
                num_transaction = int(line.split(" ")[3])
                if num_transaction > max:
                    max = num_transaction
                sum += num_transaction
                points.append(num_transaction)
            avg += sum / av
        avg /= 3
        print("{} node, n = {} ====> avg: {}, max: {}".format(_node, _n_value, round(avg, 2), max))

print('==========')

nodes = [200, 300]
time = [1, 2, 3]
for _node in nodes:
    max = 0
    avg = 0
    for _time in time:
        file_name = 'dpos-{}-{}'.format(_node, _time)
        f = open(file_name, 'r')
        sum = 0
        av = 0
        points=[]
        for line in f:
            av += 1
            num_transaction = int(line.split(" ")[3])
            if num_transaction > max:
                max = num_transaction
            sum += num_transaction
            points.append(num_transaction)
        avg += sum / av
    avg /= 3
    print("{} node ====> avg: {}, max: {}".format(_node, round(avg, 2), max))