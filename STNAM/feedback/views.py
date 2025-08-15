# feedback/views.py
from rest_framework import generics, permissions
from .models import Feedback
from .serializers import FeedbackSerializer

class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        to_user_id = self.request.data.get('to_user_id')
        serializer.save(from_user=self.request.user, to_user_id=to_user_id)


class UserFeedbackListView(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Feedback.objects.filter(to_user_id=user_id).order_by('-created_at')
