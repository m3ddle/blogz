import hashlib
import random
import string


# This will add a salt at a random index in the password then check for the salted pass hash
# as many times as necessary to match them

def make_salt():
    return ''.join(random.choice(string.ascii_letters) for x in range(5))


def salt_pass(password, salt=None):
    if not salt:
        salt = make_salt()

    insertion_point = random.randint(0, len(password) - 1)

    salty_pass = []

    for i in range(len(password)):

        if i == insertion_point:
            for j in salt:
                salty_pass += j
        salty_pass += password[i]

    return f"{''.join(salty_pass)},{salt}"


def make_hash(password, salt=None):

    salted_pass = salt_pass(password)

    hash = hashlib.sha256(str.encode(salted_pass[0])).hexdigest()

    return f"{hash},{salted_pass[1]}"


def check_hash(password, hash):
    salt = hash.split(",")[1]

    salt_check = []
    pass_list = password.split()

    for i in range(len(password) + 1):
        salt_check += password[:i]

        salt_check += salt

        salt_check += password[i:]

        if hashlib.sha256(str.encode(''.join(salt_check))).hexdigest() == hash.split(",")[0]:
            return True
        else:
            salt_check = []
    return False


def make_pw_hash(password, salt=None):
    if not salt:
        salt = make_salt()
    hash = hashlib.sha256(str.encode(password + salt)).hexdigest()
    return f'{hash},{salt}'


def check_pw_hash(password, hash):
    salt = hash.split(',')[1]
    if make_pw_hash(password, salt) == hash:
        return True

    return False


if __name__ == "__main__":
    print(check_hash(
        "aaaa", "cb1a539cd4e9b397b27d1e6cac6c9f41eb9bbe3de3d1eddef420972bf5c3e506,ytVQr"))
