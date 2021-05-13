from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.http import HttpResponseRedirect

from .models import PasswordResetRequest


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("whiteboard_app:index"))
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            dj_login(request, user)
            return HttpResponseRedirect(reverse("whiteboard_app:index"))
        else:
            context = {"error": "Bad username or password."}

    return render(request, "login_app/login.html", context)


def logout(request):
    dj_logout(request)
    return HttpResponseRedirect(reverse("login_app:login"))


def password_reset(request):
    context = {}

    if request.method == "POST":
        email = request.POST["email"]
        user = User.objects.get(email=email)
        reset_request = PasswordResetRequest()
        reset_request.user = user
        reset_request.save()
        # The password reset request creates a secret, which is turned into a
        # clickable URL, which only works for a specific user
        url = reverse(
            "login_app:password_reset_secret", args=[f"{reset_request.secret}"]
        )
        url = f'{request.scheme}://{request.META["HTTP_HOST"]}{url}'

        # I removed the code for sending "real" emails, but the print in the
        # terminal will do the same job
        print(url)
        context = {
            "message": "Please click the link in the email we sent to your email."}

    return render(request, "login_app/password_reset.html", context)


def password_reset_secret(request, secret):
    context = {"secret": secret}
    return render(request, "login_app/password_reset_form.html", context)


def password_reset_form(request):
    email = request.POST["email"]
    password = request.POST["password"]
    confirm_password = request.POST["confirm_password"]
    secret = request.POST["secret"]
    # If the posted email matches the one on the secret, the password will
    # be changed
    user = User.objects.get(email=email)
    reset_request = PasswordResetRequest.objects.get(user=user, secret=secret)
    if password == confirm_password:
        user.set_password(password)
        user.save()
        reset_request.save()
        return HttpResponseRedirect(reverse("login_app:login"))
    context = {
        "error": "Something went wrong, try again, don't screw up this time!"}
    return render(request, "login_app/password_reset_form.html", context)
