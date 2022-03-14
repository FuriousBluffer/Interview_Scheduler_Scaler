from django.urls import path

from participants.views import GetParticipant

urlpatterns = [
    path('participant/<int:pk>/', GetParticipant.as_view(), name='participant'),
]