# Transaction.py
from Signatures import generate_keys, sign, verify


class transactions:
    # transactions should hold the list of input, output address
    # list of signatures
    # and third party verfier address
    inputs = None
    outputs = None
    signs = None
    escrow = None

    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.signs = []
        self.escrow = []

    # stores all the input transaction details (sender address and amount of transaction by sender) on a list
    def add_input(self, from_addr, amount):
        print(f"Input Transaction Amount:{amount}")
        self.inputs.append((from_addr, amount))

    # stores all the output transaction details (receiver address and amount of transaction by receiver) on a list
    def add_output(self, to_addr, amount):
        print(f"Output Transaction Amount: {amount}")
        self.outputs.append((to_addr, amount))

    # stores the address of the thrid party who verfies the transation between the sender and the receiver
    def add_escrow(self, addr):
        self.escrow.append(addr)

    # generates the signature on the basis of input transactions
    # output transactions
    # and third party presence
    def sign(self, private):
        message = self.__gather()
        # print(f"Message: {message}")
        newsig = sign(message, private)
        print(f"Signature Generated: {newsig}")
        self.signs.append(newsig)

    # Validates whether the signature generated from the transaction details and private key of sender
    # could be generated with the pair public key and the transaction details

    # Also checks various conditions in which the transaction is feasible, some of which are:
    # Receiver cannot recieve more than sent by the sender
    # sender is only able to carry transactions above 0
    # Good signature must be obtained

    def is_valid(self):
        total_in = 0
        total_out = 0
        message = self.__gather()
        for addr, amount in self.inputs:
            found = False
            for s in self.signs:
                if verify(message, s, addr):
                    found = True
            if not found:
                return False
            if amount < 0:
                return False
            total_in = total_in + amount
        for addr in self.escrow:
            found = False
            for s in self.signs:
                if verify(message, s, addr):
                    found = True
            if not found:
                return False
        for addr, amount in self.outputs:
            if amount < 0:
                return False
            total_out = total_out + amount

        if total_out > total_in:
            return False

        return True

    def __gather(self):
        data = []
        data.append(self.inputs)
        data.append(self.outputs)
        data.append(self.escrow)
        return data

    def __repr__(self):
        return "Returing Transactions"


if __name__ == "__main__":
    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()
    pr4, pu4 = generate_keys()

    print("=========================================")
    print("Possible Cases of Successful Transactions")
    print("=========================================")

    print("---------Transaction 1---------")
    print("Sender = A")
    print("Receiver = B")
    print("Sending = A1")
    print("Receiving = B1")
    transactions1 = transactions()
    transactions1.add_input(pu1, 1)
    transactions1.add_output(pu2, 1)
    transactions1.sign(pr1)

    if transactions1.is_valid():
        print("Success! transactions is valid")
    else:
        print("ERROR! transactions is invalid")

    print()
    print("---------Transaction 2---------")
    print("Sender = A,B")
    print("Receiver = C")
    print("Sending = A=2,B=2")
    print("Receiving = C=4")

    transactions2 = transactions()
    transactions2.add_input(pu1, 2)
    transactions2.add_input(pu2, 2)
    transactions2.add_output(pu3, 4)
    transactions2.sign(pr1)
    transactions2.sign(pr2)

    if transactions2.is_valid():
        print("Success! transactions is valid")
    else:
        print("ERROR! transactions is invalid")

    print()
    print("---------Transaction 3---------")
    print("Sender = C")
    print("Receiver = A")
    print("Escrow = D")
    print("Sending = C3.2")
    print("Receiving = A2.1")
    transactions3 = transactions()
    transactions3.add_input(pu3, 1.2)
    transactions3.add_output(pu1, 1.1)
    transactions3.add_escrow(pu4)
    transactions3.sign(pr3)
    transactions3.sign(pr4)

    if transactions3.is_valid():
        print("Success! transactions is valid")
    else:
        print("ERROR! transactions is invalid")

    print()
    print()
    print("=========================================")
    print("Transaction Errors")
    print("=========================================")

    print()
    print("---------Transaction 4---------")
    print("Sender = A")
    print("Receiver = B")
    print("Sending = A1")
    print("Receiving = B1")
    transactions4 = transactions()
    transactions4.add_input(pu1, 1)
    transactions4.add_output(pu2, 1)
    transactions4.sign(pr2)

    if transactions4.is_valid():
        print("Success! transactions is valid")
    else:
        print("ERROR! transactions is invalid")

    # Escrow transactions not signed by the arbiter
    print()
    print("---------Transaction 5---------")
    print("Sender = C")
    print("Receiver = A")
    print("Sending = A3")
    print("Receiving = B2")
    transactions5 = transactions()
    transactions5.add_input(pu3, 1.2)
    transactions5.add_output(pu1, 1.1)
    transactions5.add_escrow(pu4)
    transactions5.sign(pr3)

    if transactions5.is_valid():
        print("Success! transactions is valid")
    else:
        print("ERROR! transactions is invalid")

    # Two input addrs, signed by one
    print()
    print("---------Transaction 6---------")
    print("Sender = C, D")
    print("Receiver = A")
    print("Sending = C1, D0.1")
    print("Receiving = A1.1")
    transactions6 = transactions()
    transactions6.add_input(pu3, 1)
    transactions6.add_input(pu4, 0.1)
    transactions6.add_output(pu1, 1.1)
    transactions6.sign(pr3)

    if transactions6.is_valid():
        print("Success! transactions is valid")
    else:
        print("ERROR! transactions is invalid")

    # # Outputs exceed inputs
    print()
    print("---------Transaction 7---------")
    print("Sender = D")
    print("Receiver = A, B")
    print("Sending = D3.2")
    print("Receiving = A1, B4")
    transactions7 = transactions()
    transactions7.add_input(pu4, 3.2)
    transactions7.add_output(pu1, 1)
    transactions7.add_output(pu2, 4)
    transactions7.sign(pr4)
    if transactions7.is_valid():
        print("Success! transactions is valid")
    else:
        print("ERROR! transactions is invalid")

    # Negative values
    print()
    print("---------Transaction 8---------")
    print("Sender = B")
    print("Receiver = A")
    print("Sending = B-1")
    print("Receiving = A-1")
    transactions8 = transactions()
    transactions8.add_input(pu2, -1)
    transactions8.add_output(pu1, -1)
    transactions8.sign(pr2)
    if transactions8.is_valid():
        print("Success! transactions is valid")
    else:
        print("ERROR! transactions is invalid")
