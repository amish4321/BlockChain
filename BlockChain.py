# Simple Blockchain Implementation
# Blockchain to store the transaction details
# Each block consists the information regarding sender, receiver and the amount of transcation

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class BlockChain:
    data = None
    previousHash = None
    previousBlock = None

    # Initializing the Constructor
    def __init__(self, buyer, sender, amount, previousBlock):
        self.previousBlock = previousBlock
        self.sender = sender
        self.buyer = buyer
        self.amount = amount

        if previousBlock != None:
            self.previousHash = previousBlock.trans_computeHash()

    # Computing the hashes of the sender, receiver and transaction amount
    def trans_computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.sender), "utf8"))
        digest.update(bytes(str(self.buyer), "utf8"))
        digest.update(bytes(str(self.amount), "utf8"))
        digest.update(bytes(str(self.previousHash), "utf8"))
        return digest.finalize()


if __name__ == "__main__":
    # Initial Block
    sender = "Amish Sharma"
    buyer = "Feng Yu"
    amount = 1200
    # Here, None is initialized because block_1 is the starting block
    block_1 = BlockChain(buyer, sender, amount, None)

    # Second Block
    sender = "John"
    buyer = "Cena"
    amount = 345
    block_2 = BlockChain(buyer, sender, amount, block_1)

    # Third Block
    sender = "Robert"
    buyer = "Downey"
    amount = 678
    block_3 = BlockChain(buyer, sender, amount, block_2)

    # List of all the blocks after the initial block
    list_of_blocks = [block_2, block_3]

    for block in list_of_blocks:
        if block.previousBlock.trans_computeHash() == block.previousHash:
            print("Hashing operation is Correct and Successful.!!")
        else:
            print("ERROR! in Hashing.")