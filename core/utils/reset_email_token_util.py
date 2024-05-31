import random
import string


def reset_email_token(length=100, otp=None):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length))
