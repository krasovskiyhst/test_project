from rest_framework import serializers
from .models import AccessLogs


class AccessLogsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = AccessLogs