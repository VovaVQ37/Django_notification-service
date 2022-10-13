from django.core.validators import RegexValidator
from django.db import models
import pytz

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