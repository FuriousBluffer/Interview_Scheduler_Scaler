# Create your views here.
import datetime
import smtplib
import time

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, \
    UpdateAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from interviews.models import Interview
from interviews.serializers import InterviewSerializer, NewCustomInterviewSerializer
from participants.models import Participant


class GetInterview(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'webapp/dashboard.html'
    queryset = Interview.objects.all()
    serializer_class = NewCustomInterviewSerializer

    def get(self, request):
        return Response({'interviews': self.get_queryset(), 'participants': Participant.objects.all()})


class CreateInterview(CreateAPIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'webapp/addinterview.html'
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

    # def get(self, request):
    #     return Response({'serializer': self.serializer_class})

    def post(self, request, *args, **kwargs):
        data = request.data
        if data['end_time'] <= data['start_time']:
            return Response("Let the interview begin before ending it")
        serializer = self.serializer_class(data=data, many=False)
        participants = data['participants']
        if len(participants) < 2:
            return Response("A minimum of 2 participants is required")
        for i in participants:
            participant = Participant.objects.get(id=i)
            individual_interviews = participant.interview_set.all()
            for j in individual_interviews.values():
                if (j['end_time'] > datetime.datetime.strptime(data['start_time'], '%H:%M').time() >= j[
                    'start_time']) or (
                        j['end_time'] >= datetime.datetime.strptime(data['end_time'], '%H:%M').time() > j[
                    'start_time']) or (
                        datetime.datetime.strptime(data['start_time'], '%H:%M').time() <= j['start_time'] and j[
                    'end_time'] <= datetime.datetime.strptime(data['end_time'], '%H:%M').time()):
                    return Response('Interview Conflict exists')
        if serializer.is_valid():
            smtp_server = "smtp-relay.sendinblue.com"
            port = 587  # For starttls
            sender_email = "spams9916@gmail.com"
            password = "8hb2qFtwNnUBT0MP"
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()  # Can be omitted
            server.starttls()
            server.ehlo()
            server.login(sender_email, password)
            for i in participants:
                participant = Participant.objects.get(id=i)
                receiver_email = participant.email
                message = f"Subject: Interview Schedule\n\nHey {participant.name},\n\n" \
                          f"You have an interview scheduled from {data['start_time']} to {data['end_time']}.\n\n" \
                          f"Regards,\nAdmin"
                server.sendmail(sender_email, receiver_email, message)
            server.quit()
            serializer.save()
            return redirect(to='interviews')


class UpdateInterview(RetrieveUpdateAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

    def put(self, request, *args, **kwargs):
        data = request.data
        if len(data['participants']) < 2:
            return Response({"status": "error", "message": "A minimum of 2 participants is required"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        interview = self.get_object()
        if data['end_time'] <= data['start_time']:
            return Response({"status": "error", "message": "Let the interview begin before ending it"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = self.serializer_class(interview, data=data, many=False)
        participants = data['participants']
        for i in participants:
            participant = Participant.objects.get(id=i)
            individual_interviews = participant.interview_set.all()
            for j in individual_interviews.values():
                if j['id'] == interview.pk:
                    continue
                # print(type(data['start_time']))
                # print(type(j['start_time']))
                if (j['end_time'] > datetime.datetime.strptime(data['start_time'], '%H:%M').time() >= j[
                    'start_time']) or (
                        j['end_time'] >= datetime.datetime.strptime(data['end_time'], '%H:%M').time() > j[
                    'start_time']) or (
                        datetime.datetime.strptime(data['start_time'], '%H:%M').time() <= j['start_time'] and j[
                    'end_time'] <= datetime.datetime.strptime(data['end_time'], '%H:%M').time()):
                    return Response({'status': "error", 'message': 'Interview Conflict exists'},
                                    status=status.HTTP_409_CONFLICT)
        if serializer.is_valid():
            smtp_server = "smtp-relay.sendinblue.com"
            port = 587  # For starttls
            sender_email = "spams9916@gmail.com"
            password = "8hb2qFtwNnUBT0MP"
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()  # Can be omitted
            server.starttls()
            server.ehlo()
            server.login(sender_email, password)
            for i in participants:
                participant = Participant.objects.get(id=i)
                receiver_email = participant.email
                message = f"Subject: Interview Schedule\n\nHey {participant.name},\n\n" \
                          f"You have an interview scheduled from {data['start_time']} to {data['end_time']}.\n\n" \
                          f"Regards,\nAdmin"
                server.sendmail(sender_email, receiver_email, message)
            server.quit()
            serializer.save()
            return Response(serializer.data)


class RetrieveInterview(RetrieveAPIView):
    queryset = Interview.objects.all()
    serializer_class = NewCustomInterviewSerializer


class DeleteInterview(DestroyAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

# def minimum_participants(sender, **kwargs):
#     if len(kwargs['pk_set']) < 2:
#         raise ValidationError("A Minimum of 2 Participants are required to schedule an interview")


# m2m_changed.connect(minimum_participants, sender=Interview.participants.through)
