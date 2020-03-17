import hashlib

import random

random = random.SystemRandom()


def get_random_string(
    length=12,
    allowed_chars=(
        "abcdefghijklmnopqrstuvwxyz",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "0123456789",
    )
):
    """
    Returns a securely generated random string.

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits.

    Taken from the django.utils.crypto module.
    """
    return "".join(random.choice(allowed_chars) for i in range(length))


def get_secret_key():
    """
    Create a random secret key.

    Taken from the Django project.
    """
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    return get_random_string(50, chars)


def get_salt():
    """
    Create a random salt for database use.
    """
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    return get_random_string(30, chars)


def gen_super_secret(key, salt):
    combo_super_secret = key + salt
    hashed_super_secret = hashlib.sha512(
        combo_super_secret.encode("utf-8")
    ).digest()

    """
    iterations = random.randint(1000, 3000)
    for i in range(iterations):
        hashed_super_secret = hashlib.sha512(
            hashed_super_secret.encode('utf-8')
        ).digest()
    """
    return hashed_super_secret


def gen_new_super_secret():
    key = get_secret_key()
    # This is somewhat redundant, but does lessen collisions for keys,
    # and does somewhat increase difficulty, as it's 30 more symbols...
    salt = get_salt()

    return {
        "super_secret": gen_super_secret(key, salt),
        "key": key,
        "salt": salt
    }


def int2uni(val):
    return str(val).encode("utf-8").decode("utf-8")
