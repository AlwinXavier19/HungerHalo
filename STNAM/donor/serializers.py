from rest_framework import serializers
from .models import Donation
from receiver.models import ReceiverRequest

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'
        read_only_fields = ['donor', 'status', 'created_at']
# receiver/serializers.py
class ReceiverRequestSerializer(serializers.ModelSerializer):
    receiver_name = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = ReceiverRequest
        fields = ['id', 'donation', 'receiver', 'receiver_name', 'status', 'timestamp']
        read_only_fields = ['receiver', 'status']
