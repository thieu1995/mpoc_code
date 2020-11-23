class Blockchain:
    def __init__(self, blockchain=None):
        self.blockchain = blockchain
    
    def add_new_block(self, block):
        self.blockchain.append(block)
