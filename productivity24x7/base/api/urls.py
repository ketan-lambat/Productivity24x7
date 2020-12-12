from django.urls import include, path
from . import views

urlpatterns = [
    path('event', views.EventBasic.as_view()),
    path('tags', views.TagBasic.as_view()),
    path('tags/<str:name>', views.TagDetail.as_view()),
    path('task', views.TaskBasic.as_view()),
    path('task/<int:idd>', views.TaskDetails.as_view()),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
