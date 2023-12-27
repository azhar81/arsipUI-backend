from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    CONTRIBUTOR = "contributor"
    VERIFICATOR = "verificator"

    USERTYPE_CHOICES = [
        (CONTRIBUTOR, "Contributor"),
        (VERIFICATOR, "Verificator"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=11, choices=USERTYPE_CHOICES)

    def __str__(self):
        return self.user.username
