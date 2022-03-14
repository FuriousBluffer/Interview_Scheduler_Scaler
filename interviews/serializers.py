from rest_framework.relations import SlugRelatedField, HyperlinkedIdentityField, StringRelatedField, \
    PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from interviews.models import Interview


class InterviewSerializer(ModelSerializer):
    # participants = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Interview
        fields = '__all__'


class CustomInterviewSerializer(ModelSerializer):
    class Meta:
        model = Interview
        fields = ('start_time', 'end_time')
