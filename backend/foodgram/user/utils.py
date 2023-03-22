from rest_framework_simplejwt.tokens import RefreshToken

def create_jwt_token(user):
    return str(RefreshToken.for_user(user).access_token)
