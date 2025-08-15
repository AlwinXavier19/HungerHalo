# feedback/urls.py
from django.urls import path
from .views import FeedbackCreateView, UserFeedbackListView

urlpatterns = [
    path('create/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('user/<int:user_id>/', UserFeedbackListView.as_view(), name='user-feedback'),
]

