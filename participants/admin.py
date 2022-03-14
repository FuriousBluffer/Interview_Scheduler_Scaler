from django.contrib import admin

# Register your models here.
from participants.models import Participant

admin.site.register(Participant)
