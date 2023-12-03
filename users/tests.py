from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


def create_contributor(username, password):
    user = User.objects.create_user(username=username, password=password)
    contributor = UserProfile.objects.create(user=user, user_type="contributor")

    return user

def create_verificator(username, password):
    user = User.objects.create_user(username=username, password=password)
    contributor = UserProfile.objects.create(user=user, user_type="verificator")

    return user
