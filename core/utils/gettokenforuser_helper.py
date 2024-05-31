from rest_framework_jwt.settings import api_settings


def get_tokens_for_user(user):
    payload = api_settings.JWT_PAYLOAD_HANDLER(user)

    # Encode payload to get the access token
    access_token = api_settings.JWT_ENCODE_HANDLER(payload)

    # Generate refresh token
    refresh_token = api_settings.JWT_REFRESH_HANDLER(access_token)
    print(refresh_token)
    print(access_token)

    return {
        'refresh': refresh_token,
        'access': access_token,
    }
