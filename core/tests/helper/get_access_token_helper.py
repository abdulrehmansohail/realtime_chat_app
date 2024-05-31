from rest_framework_simplejwt.tokens import AccessToken


def generate_access_token(user):
    access_token = AccessToken.for_user(user)
    return str(access_token)
