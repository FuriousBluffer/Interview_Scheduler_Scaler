from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.


class Interview(models.Model):
    participants = models.ManyToManyField("participants.Participant")
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["start_time", "end_time"]

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"
