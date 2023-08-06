from enum         import Enum, auto, unique
from ecdsa.curves import SECP256k1
from ecdsa.ecdsa  import generator_secp256k1, int_to_string, string_to_int


@unique
class EcdsaCurves(Enum):
    SECP256K1 = auto(),


class EcdsaFactory:
    @staticmethod
    def Create(curve_type):
        if curve_type == EcdsaCurves.SECP256K1:
            return EcdsaSecp256k1()
        else:
            return None


class EcdsaSecp256k1:
    @staticmethod
    def CurveOrder():
        return generator_secp256k1.order()

    @staticmethod
    def Generator():
        return generator_secp256k1


class EcdsaPublicKey:
    @staticmethod
    def FromSecret(secret):
        try:
            return ecdsa.VerifyingKey.from_string(secret, curve = SECP256k1)
        except ecdsa.keys.MalformedPointError:
            raise Bip32KeyError("Invalid public key (malformed point)")

    @staticmethod
    def FromPoint(point):
        try:
            return ecdsa.VerifyingKey.from_public_point(point, curve = SECP256k1)
        except:
            raise Bip32KeyError("Computed public child key is not valid, very unlucky index")


class EcdsaPrivateKey:
    @staticmethod
    def FromSecret(secret):
        try:
            return ecdsa.SigningKey.from_string(secret, curve = SECP256k1)
        except ecdsa.keys.MalformedPointError:
            raise Bip32KeyError("Invalid private key (malformed point)")
