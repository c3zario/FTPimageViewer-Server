from cryptography.hazmat.primitives import serialization
import jwt

private_key = open(".ssh/id_rsa", "r").read()
privKey = serialization.load_ssh_private_key(private_key.encode(), password=b'')
token = jwt.encode(
    payload={"body": ""},
    key=privKey,
    algorithm="RS256"
)

print("token:", token)


try:
    public_key = open(".ssh/id_rsa.pub", "r").read()
    key = serialization.load_ssh_public_key(public_key.encode())

    print("reading test:", jwt.decode(token, key, algorithms=[jwt.get_unverified_header(token)["alg"], ]))
except Exception as error:
    print("error", error)