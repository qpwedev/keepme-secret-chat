import os
import hashlib

# Default p and g values
p = 0xe3ee22210409a9b124f04d0c230e50178dd46ab92c8f2082d4b6729b2ec6f2c696f4a77e7ea7523fc5195cdd4b2a53d972073226d6c26bb34d0af89f7d6bff087f4d763aeb29ef3b1fdf67fd5a8d6b734eafab02709749be860e37e420ba14fea986226d5eecff50dd96d54b4bef41456f257d43668728408727e30fc83f73e210f7e73f0213b420e6570df698ecab71c924544cb25f0529d844f7238f46823e9b73dc4e7c01a54b64c887378a8099621fbecc2aeb0db2bf2898b98b7b05287d4372132b6d6556330254df4aafbbd9275bb953de5da2280c9ba1cd9fe79fda196ec4be899916e1d077bb1c57614cef9bad92008e41e26f0ae2057f0841f1e9ef
g = 2


# Uncomment the following lines to generate new parameters and share them with the other node
# Agree on the values of p and g
# parameters = dh.generate_parameters(generator=2, key_size=2048)
# p = parameters.parameter_numbers().p
# g = parameters.parameter_numbers().g

# print("p:", hex(p))
# print("g:", hex(g))


def generate_key(p: int, g: int):
    a = int.from_bytes(os.urandom(32), byteorder='big') % (p - 1)
    A = pow(g, a, p)
    return a, A


def validate_public_key_range(p: int, A: int) -> bool:
    return A > 1 and A < p


def validate_public_key(p: int, A: int) -> None | Exception:
    if not validate_public_key_range(p, A):
        raise Exception('Invalid public key')


def calculate_shared_secret(p, a, B) -> bytes:
    s = pow(B, a, p)
    s_bytes = s.to_bytes((s.bit_length() + 7) // 8, byteorder='big')
    shared_secret = hashlib.sha256(s_bytes).digest()
    return shared_secret
