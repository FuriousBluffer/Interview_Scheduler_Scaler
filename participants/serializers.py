from rest_framework.serializers import ModelSerializer

from participants.models import Participant


class ParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'name')


class CustomParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'


class DetailedParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'resume')
