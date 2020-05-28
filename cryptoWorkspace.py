from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def generate_keys():
	priv_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
	pub_key = priv_key.public_key()
	return priv_key, pub_key


def encrypt(msg, key):
	enc = key.encrypt(msg,
					  padding.OAEP(
						  mgf=padding.MGF1(algorithm=hashes.SHA256()),
						  algorithm=hashes.SHA256(),
						  label=None
					  ))
	return enc


def decrypt(msg, key):
	dc = key.decrypt(msg,
					 padding.OAEP(
						 mgf=padding.MGF1(algorithm=hashes.SHA256()),
						 algorithm=hashes.SHA256(),
						 label=None
					 ))
	return dc


priv,pub = generate_keys()
msg = encrypt(b"test", pub)
print(decrypt(msg, priv))
