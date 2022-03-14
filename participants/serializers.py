from rest_framework.serializers import ModelSerializer

from participants.models import Participant


class ParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
