from rest_framework import serializers
from rest_framework.serializers import Serializer


class MicroBlogPostSerializer(Serializer):
    positive_rate = serializers.IntegerField(read_only=True)

    def update(self, instance, validated_data):
        instance.positive_rate += 1
        instance.save()
        return instance
