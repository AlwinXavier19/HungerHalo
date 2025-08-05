from rest_framework import serializers
from .models import ReceiverRequest

class ReceiverRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiverRequest
        fields = '__all__'
        read_only_fields = ['receiver', 'status', 'requested_at']
# receiver/serializers.py
from rest_framework import serializers
from .models import ReceiverProfile


class ReceiverProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = ReceiverProfile
        fields = ['name', 'email', 'phone', 'address']


