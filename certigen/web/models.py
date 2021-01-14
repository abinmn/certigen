from django.db import models
from django.contrib.auth.models import Group


class Event(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Email(models.Model):
    subject = models.CharField(max_length=78)
    body_plain_text = models.TextField()
    body_html_text = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='email_attachment', blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.event.name}: {self.subject}'


class Certificate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)

    name_x_cordinate = models.FloatField(blank=True, null=True)
    name_y_cordinate = models.FloatField(blank=True, null=True)

    event_x_cordinate = models.FloatField(blank=True, null=True)
    event_y_cordinate = models.FloatField(blank=True, null=True)

    college_x_cordinate = models.FloatField(blank=True, null=True)
    college_y_cordinate = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.event.name
