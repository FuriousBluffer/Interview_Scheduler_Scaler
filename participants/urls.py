from django.urls import path

from participants.views import GetParticipants, ResumeUpdate

urlpatterns = [
    path('', GetParticipants.as_view(), name='participants'),
    path('resume/<int:pk>/', ResumeUpdate.as_view(), name='resume'),
]