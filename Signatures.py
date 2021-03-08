#Signatures.py
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

def generate_keys():
    private = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public = private.public_key()
    return private, public

def sign(message, private):
    message = bytes(str(message), 'utf-8')
    sig = private.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return sig

def verify(message, sig, public):
    message = bytes(str(message), 'utf-8')
    try:
        public.verify(
            sig,
            message,
            padding.PSS(
              mgf=padding.MGF1(hashes.SHA256()),
              salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    except:
        return False


if __name__ == '__main__':
    # Generating the Private and Public Keys
    private_key, public_key = generate_keys()
    print(f"Private Key: {private_key}")
    print(f"Public Key: {public_key}")

    # Taking message as input and creating signature
    message = str(input("Enter a message: "))
    signature = sign(message, private_key)
    print(f"Signature: {signature}")

    # Validating the Signature and Message
    right = verify(message, signature, public_key)

    if right:
        print("Validation Success!!!")
    else:
        print ("ERROR!!!")

    # Message Tampering
    message = message + "5"

    tamper_check = verify(message,signature,public_key)

    if tamper_check:
        print("Message Tampering Successful")
    else:
        print("Message Tampering not Possible")

    # Using different keys
    new_pri, new_pub = generate_keys()
    msg = "Hello, I am Amish"
    signature = sign(msg, new_pri)
    key_tamper = verify(msg, signature, public_key)

    if key_tamper:
        print("Tampering Key, Successful!!!")
    else:
        print("Tampering Key, Not Possible!!!")
