# BlockChain.py
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class BlockChain:
    data = None
    previousHash = None
    previousBlock = None

    def __init__(self, data, previousBlock):
        self.data = data
        self.previousBlock = previousBlock
        if previousBlock != None:
            self.previousHash = previousBlock.trans_computeHash()

    def trans_computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), "utf8"))
        digest.update(bytes(str(self.previousHash), "utf8"))
        return digest.finalize()

    def is_valid(self):
        if self.previousBlock == None:
            return True
        return self.previousBlock.trans_computeHash() == self.previousHash


if __name__ == "__main__":
    # Initial Block
    sender = "Amish Sharma"
    buyer = "Feng Yu"
    amount = 1200
    details = sender + buyer + str(amount)
    # Here, None is initialized because block_1 is the starting block
    block_1 = BlockChain(details, None)

    # Second Block
    sender = "John"
    buyer = "Cena"
    amount = 345
    details = sender + buyer + str(amount)
    block_2 = BlockChain(details, block_1)

    # Third Block
    sender = "Robert"
    buyer = "Downey"
    amount = 678
    details = sender + buyer + str(amount)
    block_3 = BlockChain(details, block_2)

    # List of all the blocks after the initial block
    list_of_blocks = [block_2, block_3]

    for block in list_of_blocks:
        if block.previousBlock.trans_computeHash() == block.previousHash:
            print("Hashing operation is Correct and Successful.!!")
        else:
            print("ERROR! in Hashing.")