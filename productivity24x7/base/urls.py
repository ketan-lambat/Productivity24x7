from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.homepage_view, name='home'),
    path('api/', include('base.api.urls')),
    path('auth/', include('register.urls')),

]
