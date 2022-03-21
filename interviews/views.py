# Create your views here.
import datetime
import smtplib

from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from interviews.models import Interview
from interviews.serializers import InterviewSerializer, NewCustomInterviewSerializer
from participants.models import Participant


def interview_conflict_exists(j, data):
    naive = datetime.datetime.replace(tzinfo=None)
    if (j['end_time'] > naive.strptime(data['start_time'], '%Y-%m-%dT%H:%M') >= j['start_time']) or (
            j['end_time'] >= naive.strptime(data['end_time'], '%Y-%m-%dT%H:%M') > j['start_time']) or (
            naive.strptime(data['start_time'], '%Y-%m-%dT%H:%M') <= j['start_time'] and j['end_time'] <=
            naive.strptime(data['end_time'], '%Y-%m-%dT%H:%M')):
        return True
    else:
        return False


class GetInterview(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'webapp/dashboard.html'
    queryset = Interview.objects.all()
    serializer_class = NewCustomInterviewSerializer

    def get(self, request):
        return Response({'interviews': self.get_queryset(), 'participants': Participant.objects.all()})




class CreateInterview(CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'webapp/addinterview.html'
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

    def get(self, request):
        return Response({'participants': Participant.objects.all()})

    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        data['start_time'] = data['start_time'][0]
        data['end_time'] = data['end_time'][0]
        # print(data['start_time'][0])
        # print(type(data['start_time'][0]))
        if data['end_time'] <= data['start_time']:
            return Response({"message": "Let the interview begin before ending it",
                             'participants': Participant.objects.all()})
        serializer = self.serializer_class(data=data, many=False)
        if 'participants' not in data:
            return Response({"message": "A minimum of 2 participants is required",
                             'participants': Participant.objects.all()})
        if len(data['participants']) < 2:
            return Response({"message": "A minimum of 2 participants is required",
                             'participants': Participant.objects.all()})
        participants = data['participants']

        for i in participants:
            participant = Participant.objects.get(id=i)
            individual_interviews = participant.interview_set.all()
            for j in individual_interviews.values():
                if interview_conflict_exists(j, data):
                    return Response({'message': 'Interview Conflict exists',
                                     'participants': Participant.objects.all()})
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
        else:
            print(serializer.data)
            return HttpResponse(serializer.data)


class UpdateInterview(UpdateAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'webapp/updateInterview.html'

    def get(self, request, *args, **kwargs):
        return Response({'interview': self.get_object(),
                         'participants': Participant.objects.all()})
        # return Response({'serializer': self.serializer_class, 'interview': self.get_object()})

    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        data['start_time'] = data['start_time'][0]
        data['end_time'] = data['end_time'][0]
        if data['end_time'] <= data['start_time']:
            return Response({"message": "Let the interview begin before ending it",
                             'participants': Participant.objects.all(),
                             'interview': self.get_object()},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        if 'participants' not in data:
            return Response({"message": "A minimum of 2 participants is required",
                             'participants': Participant.objects.all(),
                             'interview': self.get_object()})
        if len(data['participants']) < 2:
            return Response({"message": "A minimum of 2 participants is required",
                             'participants': Participant.objects.all(),
                             'interview': self.get_object()})
        interview = self.get_object()
        serializer = self.serializer_class(interview, data=data, many=False)
        participants = data['participants']
        for i in participants:
            participant = Participant.objects.get(id=i)
            individual_interviews = participant.interview_set.all()
            for j in individual_interviews.values():
                if j['id'] == interview.pk:
                    continue
                if interview_conflict_exists(j, data):
                    return Response({'message': 'Interview Conflict exists',
                                     'participants': Participant.objects.all(),
                                     'interview': self.get_object()})
        if serializer.is_valid():
            try:
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
            except:
                print("Mails not sent")
            serializer.save()
            return redirect(to='interviews')


def trial(request, pk):
    self = Interview.objects.get(id=pk)
    data = request.data
    if data['end_time'] <= data['start_time']:
        return Response({"message": "Let the interview begin before ending it",
                         'participants': Participant.objects.all()},
                        status=status.HTTP_406_NOT_ACCEPTABLE)
    if 'participants' not in data:
        return Response({"message": "A minimum of 2 participants is required",
                         'participants': Participant.objects.all()})
    if len(data['participants']) < 2:
        return Response({"message": "A minimum of 2 participants is required",
                         'participants': Participant.objects.all()})
    interview = self
    serializer = InterviewSerializer(interview, data=data, many=False)
    participants = data['participants']
    for i in participants:
        participant = Participant.objects.get(id=i)
        individual_interviews = participant.interview_set.all()
        for j in individual_interviews.values():
            if j['id'] == interview.pk:
                continue
            if interview_conflict_exists(j, data):
                return Response({'message': 'Interview Conflict exists',
                                 'participants': Participant.objects.all()})
    if serializer.is_valid():
        try:
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
        except:
            print("Mails not sent")
        serializer.save()
        return redirect(to='interviews')


class RetrieveInterview(RetrieveAPIView):
    queryset = Interview.objects.all()
    serializer_class = NewCustomInterviewSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'webapp/viewInterview.html'

    def get(self, request, *args, **kwargs):
        return Response({'interview': self.get_object()})


class DeleteInterview(DestroyAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer

# def minimum_participants(sender, **kwargs):
#     if len(kwargs['pk_set']) < 2:
#         raise ValidationError("A Minimum of 2 Participants are required to schedule an interview")


# m2m_changed.connect(minimum_participants, sender=Interview.participants.through)
