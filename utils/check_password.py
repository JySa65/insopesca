from django.contrib.auth import authenticate

def checkPassword(user, password):
    return authenticate(email=user, password=password)
    