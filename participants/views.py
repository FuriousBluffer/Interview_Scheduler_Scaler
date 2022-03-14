# Create your views here.
from rest_framework.generics import ListAPIView, CreateAPIView

from participants.models import Participant
from participants.serializers import ParticipantSerializer, CustomParticipantSerializer


class GetParticipants(ListAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class CreateParticipants(CreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = CustomParticipantSerializer
