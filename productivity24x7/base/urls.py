from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.homepage_view, name='home'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
    path('api/', include('base.api.urls')),
]
