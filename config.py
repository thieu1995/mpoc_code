import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    CORE_DATA_DIR = '{}/{}'.format(basedir, 'core_data')
    LOG = '{}/log'.format(CORE_DATA_DIR)
    METAHEURISTIC_METHOD = 'hsgo'  # ga, pso, woa, hsgo
    CONSENSUS_METHOD = 'mdpos'  # pos, dpos, mdpos


class BlockchainNetworkConfig(Config):
    NUM_TRANSACTION_PER_BLOCK = 2
    INITIATE_NODE_INFORMATION = [{'api_port': 8080, 'peerport': 8000, 'address': '1NsY9UvUfhsned5JVsYapkAiWMmwisgDtc', 'hostname': 'node_0'},
                                 {'api_port': 8081, 'peerport': 8001, 'address': '1Mcq9JcF7bzdCVaENbvudWvG7fuTbERwYy', 'hostname': 'node_1'},
                                 {'api_port': 8082, 'peerport': 8002, 'address': '19FQaC3GsJp9BcPDSKuGNCMWMbZjUV1Aak', 'hostname': 'node_2'},
                                 {'api_port': 8083, 'peerport': 8003, 'address': '1BwKW6VrqDT2bGw7edavfrKXR4cUVJktLG', 'hostname': 'node_3'},
                                 {'api_port': 8084, 'peerport': 8004, 'address': '17VJUZTg6HW4nL9fjxkg9oaFYbS3vipnET', 'hostname': 'node_4'}]
    INITIATE_ADDRESS = ['184EgqYxwa8SYLVrbhwBPSKxQezhKvhpVu', '1AbhyBSTc5Ksv4SFJGGAqBoyS6AxERfFMT', '1A4omxCwNnZL5PBJX4jpEG9KUciWF8VLML',
                        '127E6WbQqaPnUSiRYPU3G53KA1hCkHXD4e', '1K5pX58AegRP6F7wqgayFuDZo3mvNB6Q4f', '17sSgC9GMCgebxevGfQJZJv8w1BCVHh7fj',
                        '1LVtfHwa91Eemxh1A3Nivje5VQAgWDBCDE', '1AkAMj6TSbbJxUKCLdi9nMKoQh7WmZNEf5', '15D2FAGSgc72FkEcgfuBUkkBczvny2mJev',
                        '1GD1QsQBxy54pTHg4pQghoAf3XJ9JNK1PL', '1QKRyFaSrgTzgGbdxSs8ULxTiXwyxZTppa', '14tsyiRRyENtJCHwTF8KZPVUW2V6yocjT7',
                        '1CQvJo5wjMgw4bKHNoGxAmhuT4LJpRyW7K', '1BCiafWR5dbueaGTNeBdCPMvjQ2Qi4TvRV', '14yhhcLh35VTbEjmjqmW83p1Z2YKzkMGKx',
                        '1CwNvDzPG53DZWpBkA7XremKfPtJa9u5Mw', '1L7a1TVcgMageucuhAny2hjKSssJfZtP5j', '15xREeCNkWZRNihC7wgFCYzN5NfEPgsBS7',
                        '1Gx9hakSFQkdXc4AKsfbKmR4NnzwVSh8wn', '1LeCzWJqrubDNh3tbvAjHvTnntBYzVbgB8', '1CP1GSc3ULWEJHS9qBLnwRdUcpyJGmNBpt',
                        '13a8yo9BcZcWoP5Ki6Y2L1MmKsZMRUk25B', '12NdK2zq5jt65ZA5yU276nnSHC4zZFpndC', '1AV1KBdCo7XAkGqUFd1kczFGXJ8WXj8ujf',
                        '12S7dX2aEucfyd5ZJyn4DN177yFWNwbRxJ', '184iW7R8ZFCpYW5ADfGAphCFGYy3JUqmuh', '1K2VSLaizZoQs5uwMRwC9UGe5uDqyfWiVi',
                        '1MaaYkELtzNmbAU41nVUJFZ1R9GLdh41wG', '18nkppLtVGyMXR6sVScbRWNVNFcdBe6qE2', '13Cm1d13HMDMG8HGDptJJFMH98byD9Sg5V',
                        '1GWCCdvi4k8ixitxW6fE8BWTFXfn45sRX3', '1BSuBrYCvHNUz686b5uFNDUsVbk85ZJHhH', '1Ps5miVpjyj5Xrmi7wceEDwra99zdCfYmT',
                        '17Pd6GricuXcgMf5Wya5xym3zgsEGHueVu', '12mQbmEjY8ZcE4q7Wtwkcx2X3UxLi8jwKg', '1CuaLwakuaPxSymcAf5qL17uwNzwUaYWhm',
                        '1JDG6RbSnM8ugCR4xHnLjb6LRMA6aqu2S', '1JdtWHJgrR6Pa87Q7icM75qDfFqqcPdhxV', '1EnDb8z6XtDABzaWbyMjBkaT3e9BKChVfz',
                        '151tcBLdKnTJ3LXAj2198izSPjVs81eBVj', '18Kau1pf85ZaL2mZH7J3GQ81PTdMCk1B4Y', '12JDAk1QFbtDZE9BbabgKQgPJfN2LaxMQE',
                        '127fjsyaCbYWHArKfbZUMopQFySzSbLf9J', '164gx933wikfnn44r8hJaS2kviZsLhAfGB', '17UiX8q4nFpHtQA9VhBE9DxNJMVzSJedeX',
                        '18Dwmyy43qWTJCBBz75VC3afGRLW9XRENd', '16eJLK4ZfikMAKc8K3QecuFvMhALyiK9YH', '1BcmXfoTxQ6QpiuX3YNeDNmRtLH5XibPHQ',
                        '1Ee4Ty7StTrWkWjcAoEsFS7NdcUEeDFUWj', '19hTx6QLKpVqPmUnaNGkmax6pXWNTiqtTt', '1M163GRyQc3QTNHWHcoRcm2XEQkDDU2ATY',
                        '1E1J24rxPeQKXFXEzFEsv3P5UJdzjsRmML', '1NDrJEHHx8ZyCak5a2wXk21GPRXqAbgLJD', '1L3Dp45KoFcvR3Z6bDzfCGHCCp9hj1CFSi',
                        '14s5GWft1ttbj1HYdbP894t6RzSwSSP1KY', '1K3dESs57AH1FaEvvYvzQ9RzWyx4qcqzGp', '1Kgo9oC7nr16v59CW8g27ePBKF5sHta1Sh',
                        '1HS4eGENYVNA9hyiZGrdeuSD3mwAmQo51x', '12zacjWdr5Xph7ieLMRNvk3LezGLFqx7Kc', '1Aem1fvhWXVgQVT9W9W9wvsNwWi4A4M6JE',
                        '1FsiB5pmQdD5ECajAE6RsgdGK2wxRqAsaS', '18PNUZjxZo4odANyVgD4XTgr9LrSvvEUWF', '1N4cnL8mEiFf7MXywNcfu5FHt6VbXTLvkW',
                        '17NivXtHuMQMoLMvGUmFrWbaYTgLmqe8vV', '1KRwJXiDGvZW2Bx2gNJs7WLXtquFd1K9Tz', '1HsYC4yEL5ADNuitXywxcfn4ntmrz395Dy',
                        '17cQXWymyZP8Ssc6mLRNrm6uArNiQ7GCAF', '1HdXM16o74zvt5iFxfY4iYUMeK4vD8vSGn', '145oCYxGENMhgrfXkWF3RnzUF4yEnPuQoo',
                        '1H374VWSRGuRojQUR2TkVpJtTjSn2wRL7A', '162sDdwC9BpsJyXY4Yvm6xgzRZWenaPLS7', '1CUxkJxJviZfFgvNJvF1yJRg76BQtehGWN',
                        '1HDBRoHLA3NNcrEgK5mggmymk6Lv8AJPjP', '1NDURXXioKqA6RqTVHZLpWJBzYyBEZ4CtS', '1QJPuQXrBQWd1BCWUzYBbRSwWXgJb4Wzpr',
                        '1Hc6hy4jqAiaWyetEsPQ6xKg1dqr67ywYP', '1EYLempEkX9TyFg4FDq7TXzEcBUK7fMi3Y', '1GsboqPWJdN6otUhHuaDbmKeuffbxo1knm',
                        '1FFc5M2trw5KPSqioBDA9JCJGwyUwdKJFC', '1FBojfeCkL9GJyFG2MwYsoWb3qYbAohrDq', '1MkxXE3vRxF3SwUSMRZYmNTTJeTuqfnYuW',
                        '1DbJvAst5RnrLU66P4AZUXGyMpGot3SqrR', '17CXviT3zQawFfWeH3RSy7GWFMMUYBZcr', '1LKLAWLjc29dkEbPC1Yoqd3w8Coje49831',
                        '1PaLQKBYRYmrcoMru48Bks8SgLbzASYisd', '15z2U8KXvQUcdSnB2YLBtECQy62thyAisH', '17FGTianmL1s32WfWaY3s5Xxqy9vF36Ru5',
                        '1FWnZ2yZGV44N6pL9eAvVZq47GyWo9cK6E', '1DXTNr79AU6KW6eyDtXtSmy7adPjaBPJ2W', '1LcJEXEeque7VPR9g4B7t1WtB56cd3V7dR',
                        '195mKAqZeK5KeNUUAVFP4HS4hLCgRVKUka', '1Q1mw1V2Usri6GZp35j2872xBTkm1QhKnz', '147n7F8UyGG7LbZiTi4xA1gqx8288oArRv',
                        '1GXbWZ97nmNhJHuVL48jrnmE6kNiuKB6Rs', '1JEXvhPp83FkLiKKENutxpwr22PpeVE6zE', '1MLFwMP9ydFyqyDrTVq2njHutvKYVqsrEw',
                        '182rj2v8hFh3PKQsYPvzDf2fVNJEVWJJn6', '1D1yNfgwZsasQLJgxKtfgNXX4KSsC86Xrs', '1EomsBVPWP1ZCXMNBxPUtGvmchuRSNJyuR',
                        '1GpKAxaCw8ZfLSYTpAbKeDCdZQGVTV4wMy']


class DposConfig(Config):
    NUM_PEER_ON_NETWORK = 50
    NUM_ROUND = 100
    NUM_LEADER_EACH_ROUND = 11
    NUM_CANDIDATE_LEADER = 10
    NUM_PEER_IN_ROUND_1 = 20
