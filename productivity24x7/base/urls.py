from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.homepage_view, name='home'),
    path('status', views.status, name='status'),
    path('auth/', include('register.urls')),
    path('events/', views.display_calendar_events, name='events'),
    path('load_g_events/', views.get_calender_events_view, name='get_g_events'),
]
