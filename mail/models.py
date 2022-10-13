from django.core.validators import RegexValidator
import pytz
from django.db import models
from django.utils import timezone
from client.models import Client



class Mail(models.Model):
    date_start = models.DateTimeField(verbose_name='Mailing start')
    date_end = models.DateTimeField(verbose_name='End of mailing')
    time_start = models.TimeField(verbose_name='Start time to send message')
    time_end = models.TimeField(verbose_name='End time to send message')
    text = models.TextField(max_length=255)
    tag = models.CharField(max_length=100, blank=True)
    operator_code = models.CharField(max_length=3, blank=True)

    def send(self):
        now = timezone.now()
        if self.date_start <= now <= self.date_end:
            return True
        else:
            return False

    def __str__(self):
        return f'Mailing {self.id} from {self.date_start}'


class Message(models.Model):
    time_create = models.DateTimeField(auto_now_add=True)
    sending_status = models.CharField(max_length=15)
    mailing = models.ForeignKey(Mail, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f'Message {self.id} with text {self.mail} for {self.client}'


class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    phone_regex = RegexValidator(regex=r'^7\d{10}$',
                                 message="The client's phone number in the format 7XXXXXXXXXX (X - number from 0 to 9)")
    phone_number = models.CharField(validators=[phone_regex], unique=True, max_length=11)
    mobile_operator_code = models.CharField(max_length=3, editable=False)
    tag = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')

    def save(self, *args, **kwargs):
        self.mobile_operator_code = str(self.phone_number)[1:4]
        return super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f'Client {self.id} with number {self.phone_number}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'