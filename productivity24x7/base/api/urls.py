from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'reminder', views.ReminderViewSet)
router.register(r'task', views.TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
