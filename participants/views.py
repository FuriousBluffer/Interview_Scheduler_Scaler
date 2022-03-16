# Create your views here.
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from participants.models import Participant
from participants.serializers import ParticipantSerializer, CustomParticipantSerializer


class GetParticipants(ListAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class CreateParticipants(CreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = CustomParticipantSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'webapp/addParticipant.html'

    def get(self, request):
        return Response({'serializer': self.serializer_class})
