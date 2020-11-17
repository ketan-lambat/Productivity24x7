from django.urls import path

from .views import Login, Register, Logout, profile_create_form, profile_create, profile, auth_callback

urlpatterns = [
    path('login', Login.as_view(), name="login"),
    path('register', Register.as_view(), name='register'),
    path('create/<b64id>/<token>', profile_create_form, name='profile_create_form'),
    path('profile', profile_create, name='profile_create'),
    path('logout', Logout.as_view(), name='logout'),
    path('', profile, name="profile"),
    path('oauth/<provider>', auth_callback, name="auth_callback")
]
