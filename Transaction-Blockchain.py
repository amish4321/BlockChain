# Blockchain Transactions
import time
import pickle
import random
from math import floor
from BlockChain import BlockChain
from Transactions import transactions
from cryptography.hazmat.primitives import hashes
from Signatures import generate_keys, sign, verify
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# File Handling to input following
# - mining rewards
# - no. of leading zeros on output hash
f = open("sys.txt", "r")
read = f.readlines()
mine_rewards = read[0]
nonce_zeros = int(read[1])

# Blockchain Transactions Class
class BTransac(BlockChain):
    def __init__(self, previousBlock):
        # BTransac Class is in heriting from Blockchain Class using Super Class function
        super(BTransac, self).__init__([], previousBlock)

    # Transactions input
    def add_trans(self, trans_in):
        self.data.append(trans_in)

    # Couting the total no. of inputs and output demands
    def __inp_out_counter(self):
        inp_total = 0
        out_total = 0
        for tx in self.data:
            for _, amt in tx.inputs:
                inp_total = inp_total + amt
            for _, amt in tx.outputs:
                out_total = out_total + amt
        return inp_total, out_total

    # Validating if the total demand is greater than sum of input and mining rewards 
    def is_valid(self):
        if not super(BTransac, self).is_valid():
            return False
        for tx in self.data:
            if not tx.is_valid():
                print("Here")
                return False
        inp_total, out_total = self.__inp_out_counter()

        if out_total - inp_total - float(mine_rewards) > 0.0000000000000000001:
            return False

        print(f"Amount on User Account: {inp_total}")
        print(f"Amount Demanded: {out_total}")
        amount_left = float(inp_total - out_total)
        amount_two = float("{:.2f}".format(amount_left))
        print(f"Amount on user account before Mining Rewards: {amount_two}")

        return True

    # Checking if the nonces are able to generate the hash with required no. of leading zeros 
    def valid_nonce(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), "utf8"))
        digest.update(bytes(str(self.previousHash), "utf8"))
        digest.update(bytes(str(self.nonce), "utf8"))
        output_hash = digest.finalize()

        if output_hash[:nonce_zeros] != bytes("\x4f" * nonce_zeros, "utf8"):
            return False

        print(f"The Block is Mined.")
        print(f"The mining reward is: {mine_rewards}")
        return True

    # Generating different nonces until they are valid with required amount of leading zeros
    def search_nonce(self):
        for _ in range(1000):
            self.nonce = "".join(
                [chr(random.randint(0, 255)) for i in range(10 * nonce_zeros)]
            )
            if self.valid_nonce():
                print(f"The Valid Nonce is: {self.nonce}")
                return self.nonce
        return None


if __name__ == "__main__":
    # Generating private and public keys
    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()
    pr4, pu4 = generate_keys()

    # Adding the First Transaction
    print("TRANSACTION 1 Created")
    Tx1 = transactions()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)

    # Checking if the Transaction is valid or not
    if Tx1.is_valid():
        print("This is a Valid Transaction.")

    # Saving the first transaction into pickle dat file
    savefile = open("transaction.dat", "wb")
    pickle.dump(Tx1, savefile)
    savefile.close()

    # Loading the pickle dat file
    loadfile = open("transaction.dat", "rb")
    newTx = pickle.load(loadfile)

    # checking if the loaded same transation is valid or not
    if newTx.is_valid():
        print("Sucess! Loaded transaction is valid")
    loadfile.close()

    print("=" * 80)

    # Creating Blocks on the Blockchain
    # Creating the first or Genesis or the root block 
    print("Genesis Block Created.")
    root = BTransac(None)
    print("TRANSACTION 1 added to Genesis Block.")
    # Adding the first transaction on to the Genesis Block
    root.add_trans(Tx1)

    # Creating second transaction
    print("TRANSACTION 2 Created")
    Tx2 = transactions()
    Tx2.add_input(pu2, 1.1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr2)

    # Adding the second transaction to the root block
    print("TRANSACTION 2 added to Genesis Block.")
    root.add_trans(Tx2)

    if root.is_valid():
        print("The block has valid transactions")
    else:
        print("Invalid Transactions on the block.")

    print("=" * 80)

    # Creating second block
    print("Block 1 Created.")
    B1 = BTransac(root)
    print("TRANSACTION 3 Created.")
    
    # Creating third transaction
    Tx3 = transactions()
    Tx3.add_input(pu3, 1.1)
    Tx3.add_output(pu1, 1)
    Tx3.sign(pr3)

    print("TRANSACTION 3 added to Block 1.")

    Tx4 = transactions()
    Tx4.add_input(pu4, 100)
    Tx4.add_output(pu4, 99)
    Tx4.sign(pr4)


    # Adding the third transaction onto the First Block
    B1.add_trans(Tx3)
    B1.add_trans(Tx4)


    # Calculating the time period for searching the nonce with required leading zeros
    start = time.time()
    B1.search_nonce()
    end = time.time()

    print(f"Time taken to calculate Nonce: {end-start}s")

    # Checking if the nonce generated are valid or not
    if B1.valid_nonce():
        print("B1 is a Valid Nonce.")
    else:
        print("Nonce was not found for B1.")

    if B1.is_valid():
        print("The block has valid transactions")
    else:
        print("Invalid Transactions on the block.")

    # Saving the first block into a blockchain.dat file
    savefile = open("blockchain.dat", "wb")
    pickle.dump(B1, savefile)
    savefile.close()

    # Loading the saved block using Pickle
    loadfile = open("blockchain.dat", "rb")
    load_B1 = pickle.load(loadfile)


    # Checking if the loaded block has valid nonce or not 
    if load_B1.valid_nonce():
        print("Nonce is valid after saving and loading pickle.")
    else:
        print("Loaded Nonce is Invalid.")