from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from django.http import Http404
from oauth2_provider.contrib.rest_framework.permissions import TokenMatchesOASRequirements
from rest_framework.decorators import api_view

from .serializers import EventSerializer, TagSerializer, TaskSerializer, WebHookSerializer, WebHookReadSerializer
from .permissions import IsOwner
from base.models import *


@api_view(http_method_names=['GET'])
def home(request):
    host = request.scheme + "://" + request.get_host()
    return Response(data={
        'event': host + "/api/event",
        'tags': host + "/api/tags",
        'task': host + "/api/task",
        'webhooks': host + "/api/webhooks"
    }, status=status.HTTP_200_OK)


class TagBasic(ListAPIView, APIView):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(owner__pk=self.request.user.pk).all()

    permission_classes = [IsAuthenticated & (IsOwner | TokenMatchesOASRequirements)]
    required_alternate_scopes = {
        "GET": [['tags.read']],
        "POST": [['tags.add']]
    }

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetail(APIView):
    permission_classes = [IsAuthenticated & (IsOwner | TokenMatchesOASRequirements)]
    required_alternate_scopes = {
        "GET": [['tags.read']],
        "DELETE": [['tags.delete']],
        "POST": [['tags.edit'], ['tags.add', 'tags.delete']]
    }

    def get_object_or_404(self, request, name):
        try:
            obj = Tag.objects.get(owner=request.user, name=name)
        except Tag.DoesNotExist:
            raise Http404
        self.check_object_permissions(request, obj)
        return obj

    def get(self, request, name):
        obj = self.get_object_or_404(request, name)
        serializer = TagSerializer(obj)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, name):
        obj = self.get_object_or_404(request, name)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, name):
        obj = self.get_object_or_404(request, name)
        serializer = TagSerializer(instance=obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskBasic(ListAPIView, APIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(owner__pk=self.request.user.pk).all()

    permission_classes = [IsAuthenticated & (IsOwner | TokenMatchesOASRequirements)]
    required_alternate_scopes = {
        "GET": [['task.read']],
        "POST": [['task.add']]
    }

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetails(APIView):
    permission_classes = [IsAuthenticated & (IsOwner | TokenMatchesOASRequirements)]
    required_alternate_scopes = {
        "GET": [['task.read']],
        "DELETE": [['task.delete']],
        "POST": [['task.edit'], ['task.add', 'task.delete']]
    }

    def get_object_or_404(self, request, idd):
        try:
            obj = Task.objects.get(owner=request.user, pk=idd)
        except Task.DoesNotExist:
            raise Http404
        self.check_object_permissions(request, obj)
        return obj

    def get(self, request, idd):
        obj = self.get_object_or_404(request, idd)
        serializer = TaskSerializer(obj)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, idd):
        obj = self.get_object_or_404(request, idd)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, idd):
        obj = self.get_object_or_404(request, idd)
        serializer = TaskSerializer(instance=obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WebHookBasic(ListAPIView, APIView):
    serializer_class = WebHookReadSerializer

    def get_queryset(self):
        return WebHook.objects.filter(owner__pk=self.request.user.pk).all()

    permission_classes = [IsAuthenticated & (IsOwner | TokenMatchesOASRequirements)]
    required_alternate_scopes = {
        "GET": [['webhooks']],
        "POST": [['event.read', 'webhooks']]
    }

    def post(self, request):
        serializer = WebHookSerializer(data=request.data)
        if serializer.is_valid():
            s = serializer.save(owner=request.user)
            data = WebHookReadSerializer(instance=s, data={}, partial=True)
            data.is_valid()
            return Response(data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventBasic(ListAPIView, APIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(owner__pk=self.request.user.pk).all()

    permission_classes = [IsAuthenticated & (IsOwner | TokenMatchesOASRequirements)]
    required_alternate_scopes = {
        "GET": [['event.read']],
        "POST": [['event.add']]
    }

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetails(APIView):
    permission_classes = [IsAuthenticated & (IsOwner | TokenMatchesOASRequirements)]
    required_alternate_scopes = {
        "GET": [['event.read']],
        "DELETE": [['event.delete']],
        "POST": [['event.edit'], ['event.add', 'event.delete']]
    }

    def get_object_or_404(self, request, idd):
        try:
            obj = Event.objects.get(owner=request.user, pk=idd)
        except Task.DoesNotExist:
            raise Http404
        self.check_object_permissions(request, obj)
        return obj

    def get(self, request, idd):
        obj = self.get_object_or_404(request, idd)
        serializer = EventSerializer(obj)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, idd):
        obj = self.get_object_or_404(request, idd)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, idd):
        obj = self.get_object_or_404(request, idd)
        serializer = EventSerializer(instance=obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
