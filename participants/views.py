from django.shortcuts import render

# Create your views here.
from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView, RetrieveUpdateAPIView

from participants.models import Participant
from participants.serializers import ParticipantSerializer, DetailedParticipantSerializer


class GetParticipants(ListAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class ResumeUpdate(RetrieveUpdateAPIView):
    queryset = Participant.objects.all()
    serializer_class = DetailedParticipantSerializer
