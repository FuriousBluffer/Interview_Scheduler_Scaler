from django.shortcuts import render

# Create your views here.
from rest_framework.generics import RetrieveAPIView

from participants.models import Participant
from participants.serializers import ParticipantSerializer


class GetParticipant(RetrieveAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
