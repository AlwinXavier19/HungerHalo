from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import ReceiverRequest
from .serializers import ReceiverRequestSerializer
from .permissions import IsReceiver

class ReceiverRequestCreateView(generics.CreateAPIView):
    queryset = ReceiverRequest.objects.all()
    serializer_class = ReceiverRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsReceiver]

    def perform_create(self, serializer):
        serializer.save(receiver=self.request.user)


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ReceiverProfile

class UpdateReceiverProfile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'receiver':
            return Response({'error': 'Not a receiver'}, status=403)

        profile = user.receiverprofile
        profile.address = request.data.get('address', profile.address)
        profile.phone = request.data.get('phone', profile.phone)
        profile.save()

        return Response({'message': 'Profile updated'})



from .serializers import ReceiverProfileSerializer

class ReceiverProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = ReceiverProfile.objects.get(user=request.user)
            serializer = ReceiverProfileSerializer(profile)
            return Response(serializer.data)
        except ReceiverProfile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)
class ReceiverRequestStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requests = ReceiverRequest.objects.filter(receiver=request.user)
        from .serializers import ReceiverRequestSerializer
        serializer = ReceiverRequestSerializer(requests, many=True)
        return Response(serializer.data)


from rest_framework import status

from donor.models import Donation  # Import Donation model
from volunteer.models import DeliveryRequest
class ConfirmDeliveryView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, request_id):
        try:
            receiver_request = ReceiverRequest.objects.get(id=request_id, receiver=request.user)
        except ReceiverRequest.DoesNotExist:
            return Response({"error": "Request not found or you are not authorized."}, status=status.HTTP_404_NOT_FOUND)

        # 1️⃣ Update ReceiverRequest status
        receiver_request.status = 'received'
        receiver_request.save()

        # 2️⃣ Update related Donation status
        if receiver_request.donation:
            receiver_request.donation.status = 'delivered'
            receiver_request.donation.save()

            # 3️⃣ Update VolunteerDeliveryRequest status if linked
            volunteer_request = DeliveryRequest.objects.filter(donation=receiver_request.donation).first()
            if volunteer_request:
                volunteer_request.status = 'completed'
                volunteer_request.save()

        return Response({
            "message": "Status updated: ReceiverRequest -> received, Donation -> delivered, VolunteerDeliveryRequest -> completed"
        }, status=status.HTTP_200_OK)
