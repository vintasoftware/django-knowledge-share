from rest_framework import serializers
from rest_framework.serializers import Serializer


class MicroBlogPostSerializer(Serializer):
    rate = serializers.BooleanField(
        write_only=True,
    )
    positive_rate = serializers.IntegerField(read_only=True)

    def update(self, instance, validated_data):
        if validated_data['rate']:
            instance.positive_rate += 1
        instance.save()
        return instance
