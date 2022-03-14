from django.db import models


# Create your models here.

class Participant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    resume = models.FileField(null=True, blank=True, upload_to='resumes/')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
