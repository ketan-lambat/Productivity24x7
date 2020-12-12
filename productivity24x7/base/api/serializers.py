from rest_framework import serializers
from base.models import Tag, Task, Event
from django.core.exceptions import ValidationError as ValidError


class TagSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25, required=True, allow_blank=False)
    priority = serializers.IntegerField(min_value=0, required=True)
    color = serializers.ModelField(model_field=Tag()._meta.get_field('color'))

    def save_model(self, instance):
        try:
            instance.save()
        except ValidError as v:
            raise serializers.ValidationError(detail=v.error_dict)
        return instance

    def create(self, validated_data):
        t = Tag(**validated_data)
        return self.save_model(t)

    def update(self, instance, validated_data):
        t = instance
        t.color = validated_data.get('color', instance.color)
        t.priority = validated_data.get('priority', instance.priority)
        return self.save_model(t)


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    description = serializers.ModelField(Task()._meta.get_field('description'), required=False, default="")
    duration = serializers.IntegerField(min_value=0, required=False, allow_null=True)
    deadline = serializers.DateTimeField(required=False, allow_null=True)
    is_completed = serializers.BooleanField(required=False, allow_null=True)

    def save_model(self, instance):
        try:
            instance.save()
        except ValidError as v:
            raise serializers.ValidationError(detail=v.error_dict)
        return instance

    def create(self, validated_data):
        t = Task(**validated_data)
        return self.save_model(t)

    def update(self, instance, validated_data):
        t = instance
        t.title = validated_data.get('title', instance.title)
        t.description = validated_data.get('description', instance.description)
        t.duration = validated_data.get('duration', instance.duration)
        t.deadline = validated_data.get('deadline', instance.deadline)
        t.is_completed = validated_data.get('is_completed', instance.is_completed)
        return self.save_model(t)


class EventSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100, required=True)
    description = serializers.ModelField(Task()._meta.get_field('description'), required=False, default="")
    start = serializers.DateTimeField(required=True)
    end = serializers.DateTimeField(required=True)
    tags = serializers.ListField(allow_null=False, allow_empty=True,
                                 child=serializers.CharField(max_length=25, required=True, allow_blank=False))

    def save_model(self, instance):
        try:
            instance.save()
        except ValidError as v:
            raise serializers.ValidationError(detail=v.error_dict)
        return instance

    def create(self, validated_data: dict):
        tags = validated_data.get('tags', [])
        validated_data.pop('tags')
        t = Event(**validated_data)
        t.tags = tags
        return self.save_model(t)

    def update(self, instance, validated_data):
        t = instance
        t.title = validated_data.get('title', instance.title)
        t.description = validated_data.get('description', instance.description)
        t.start = validated_data.get('start', instance.start)
        t.end = validated_data.get('end', instance.end)
        t.tags = validated_data.get('tags', instance.tags)
        return self.save_model(t)
