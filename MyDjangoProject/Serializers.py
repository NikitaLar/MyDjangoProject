from rest_framework import serializers
from .models import authentication


class serialize(serializers.ModelSerializer):
    class Meta:
        model = authentication
        fields = ['id', 'username', 'password', 'emailid']


class messagserializer(serializers.Serializer):
    Response = serializers.CharField()
    Message = serializers.CharField()