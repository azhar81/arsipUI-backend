from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def my_view(request):
    # Access the user and user profile information
    user = request.user
    user_profile = user.user_type

    return JsonResponse({"user": user, "user_profile": user_profile})
