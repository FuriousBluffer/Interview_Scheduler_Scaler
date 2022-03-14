from django.urls import path

from participants.views import GetParticipants, CreateParticipants

urlpatterns = [
    path('', GetParticipants.as_view(), name='participants'),
    path('create/', CreateParticipants.as_view(), name='create_participant'),
]