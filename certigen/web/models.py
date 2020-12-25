from django.db import models
from django.contrib.auth.models import Group


class Event(models.Model):
    name = models.CharField(max_length=100)
    user_group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Email(models.Model):
    subject = models.CharField(max_length=78)
    body_plain_text = models.TextField()
    body_html_text = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='email_attachment', blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    user_group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Certificate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)

    name_x_cordinate = models.FloatField(blank=True, null=True)
    name_y_cordinate = models.FloatField(blank=True, null=True)

    event_x_cordinate = models.FloatField(blank=True, null=True)
    event_y_cordinate = models.FloatField(blank=True, null=True)

    college_x_cordinate = models.FloatField(blank=True, null=True)
    college_y_cordinate = models.FloatField(blank=True, null=True)