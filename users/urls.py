from django.urls import path
from .views import my_view

urlpatterns = [
    path("profile", my_view, name="profile"),
]
