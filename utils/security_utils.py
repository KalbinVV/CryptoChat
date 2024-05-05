import datetime
import string
import time
from random import choices

import numpy as np
from randomgen import ChaCha


def generate_common_key(seed: int, length: int, rounds: int = 8) -> bytes:
    rg = np.random.Generator(ChaCha(seed=seed, rounds=rounds))

    return rg.bytes(length)


def get_nonce() -> bytes:
    now = datetime.datetime.now()

    return str(now.minute).encode()


def get_random_session_key(length: int = 16) -> bytes:
    return ''.join(choices(string.ascii_uppercase + string.digits, k=length)).encode()
