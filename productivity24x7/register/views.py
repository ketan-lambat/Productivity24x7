from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode as b64_encode, urlsafe_base64_decode as b64_decode
from django.views import View
from django.http import HttpResponseBadRequest
from django.db import transaction
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required

from .models import User
from .generators import registration_token_gen
from .providers import *


def bad_request():
    return HttpResponseBadRequest(content="Bad Request")


def login_and_redirect(request, user):
    if not user.is_active:
        return bad_request()
    auth_login(request, user)
    if "next" in request.GET:
        return redirect(request.GET["next"])
    else:
        return redirect('profile')


def make_token(email):
    fn = str(email).split('@')[0].capitalize()
    u = User.objects.create_user(first_name=fn, email=email)
    u.set_password(None)
    u.save()
    token = registration_token_gen.make_token(u)
    b64id = b64_encode(bytes(str(u.pk).encode()))
    return token, b64id


class Login(View):
    def get(self, request):
        gh_auth, state = get_github_auth_url()
        request.session['github_oauth_state'] = state
        request.session['github_oauth_use'] = 'login'
        return render(request, 'base/login.html', context={'GITHUB_AUTH': gh_auth})

    def post(self, request):
        if 'email' in request.POST and 'password' in request.POST:
            email = request.POST["email"]
            password = request.POST["password"]
            u = authenticate(request, email=email, password=password)
            if u is None:
                return render(request, 'base/login.html', context={'error': "Invalid Email or Password."})
            else:
                return login_and_redirect(request, u)
        else:
            return bad_request()


class Logout(View):
    def get(self, request):
        auth_logout(request)
        return redirect(to='login')


def register(request, email):
    try:
        validate_email(email)
        if User.objects.get_or_none(email=email) is not None:
            raise ValueError()
    except ValidationError:
        return render(request, 'base/register.html', context={'error': "Invalid Email."})
    except ValueError:
        return render(request, 'base/register.html', context={'error': "Email already exists."})
    token, b64id = make_token(email)
    return redirect(to="profile_create_form", b64id=b64id, token=token)


class Register(View):
    def get(self, request):
        gh_auth, state = get_github_auth_url()
        request.session['github_oauth_state'] = state
        request.session['github_oauth_use'] = 'register'
        return render(request, 'base/register.html', context={'GITHUB_AUTH': gh_auth})

    @transaction.atomic()
    def post(self, request):
        if 'email' in request.POST:
            email = request.POST["email"]
            return register(request, email)
        else:
            return bad_request()


def profile_create_form(request, b64id, token):
    pk = b64_decode(b64id).decode()
    u = User.objects.get_or_none(pk=pk)
    if u is None or u.is_active:
        return bad_request()
    elif not registration_token_gen.check_token(u, token):
        return bad_request()
    else:
        return render(request, 'base/profile.html',
                      context={'email': u.email, 'first_name': u.first_name, 'last_name': u.last_name, 'b64id': b64id,
                               'token': token})


@transaction.atomic()
def profile_create(request):
    b64id = request.POST.get('b64id', None)
    token = request.POST.get('token', None)
    if b64id is None or token is None:
        return bad_request()
    pk = int(b64_decode(b64id).decode())
    u = User.objects.get_or_none(pk=pk)
    if u is None or u.is_active or not registration_token_gen.check_token(u, token):
        return bad_request()
    else:
        fn = request.POST.get('first_name', None)
        ln = request.POST.get('last_name', "")
        pwd = request.POST.get('password', None)
        re_pwd = request.POST.get('re_password', None)
        error = ""
        if fn is None or fn == "":
            error = error + "First Name is required. "
        if pwd is None or pwd == "":
            error = error + "Password is required. "
        if pwd != re_pwd:
            error = error + "Passwords must match. "
        if error == "":
            u.first_name = "Hello"
            u.last_name = ln
            u.is_active = True
            u.set_password(pwd)
            u.save()
            return redirect(to="login")
        else:
            return render(request, 'base/profile.html',
                          context={'email': u.email, 'first_name': u.first_name, 'last_name': u.last_name,
                                   'b64id': b64id,
                                   'token': token, 'error': error})


@login_required(redirect_field_name="next", login_url=reverse_lazy('login'))
def profile(request):
    return redirect(to="home")


def auth_callback(request, provider):
    if provider == 'github':
        # print(request.session['github_oauth_state'])
        if 'github_oauth_state' in request.session and 'github_oauth_use' in request.session:
            state = request.session['github_oauth_state']
            path = "https://localhost" + request.get_full_path()
            data = verify_github(path, state)
            email = data[0]['email']
            if request.session['github_oauth_use'] == 'register':
                return register(request, email)
            elif request.session['github_oauth_use'] == 'login':
                u = User.objects.get_or_none(email=email)
                if u is None:
                    return render(request, 'base/login.html', context={'error': "We cannot find that account."})
                else:
                    return login_and_redirect(request, u)
        else:
            return bad_request()
