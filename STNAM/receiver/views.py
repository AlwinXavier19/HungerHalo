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

# class ReceiverRequestListView(generics.ListAPIView):
#     serializer_class = ReceiverRequestSerializer
#     permission_classes = [permissions.IsAuthenticated, IsReceiver]

#     def get_queryset(self):
#         return ReceiverRequest.objects.filter(receiver=self.request.user)

# views.py

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

# receiver/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ReceiverProfile
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

