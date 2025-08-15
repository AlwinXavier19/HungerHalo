
from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    from_user = serializers.ReadOnlyField(source='from_user.username')
    to_user = serializers.ReadOnlyField(source='to_user.username')

    class Meta:
        model = Feedback
        fields = ['id', 'donation', 'from_user', 'to_user', 'rating', 'comment', 'created_at']
        read_only_fields = ['from_user', 'created_at']

    def validate(self, attrs):
        request_user = self.context['request'].user
        donation = attrs['donation']
        to_user_id = self.context['request'].data.get('to_user_id')

        # Check if donation is delivered
        if donation.status.lower() != 'delivered':
            raise serializers.ValidationError("You can only leave feedback after the donation is delivered.")

        # Ensure user is part of the transaction
        if request_user not in [donation.donor, donation.receiver, donation.volunteer]:
            raise serializers.ValidationError("You are not allowed to leave feedback for this donation.")

        # Ensure not reviewing themselves
        if int(to_user_id) == request_user.id:
            raise serializers.ValidationError("You cannot review yourself.")

        return attrs

