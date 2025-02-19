import base64


def encode(string):
    return base64.urlsafe_b64encode(string.encode()).rstrip(b"=").decode("utf-8")


def decode(encoded_string):
    padded_encoded_string = encoded_string + "=="[: (len(encoded_string) % 4)]
    return base64.urlsafe_b64decode(padded_encoded_string).decode()
