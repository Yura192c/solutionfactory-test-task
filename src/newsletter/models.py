from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.utils import timezone


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^7[0-9]{10}$',
                message='Phone number must be in the format 7XXXXXXXXXX'
            )
        ]
    )
    # Все российские операторы имеют код от 900 до 997, в тз не указано нужны именно российские операторы или нет
    # поэтому я ограничился этими кодами
    mobile_operator_code = models.IntegerField(
        validators=[MinValueValidator(900), MaxValueValidator(997)])
    tag = models.CharField(max_length=100)
    timezone = models.CharField(max_length=255)


class ClientFilters(models.IntegerChoices):
    '''
    Client filters for dispatch
    '''

    TAG_FILTER = 1, 'Tag filter'
    MOBILE_OPERATOR_CODE_FILTER = 2, 'Mobile operator code filter'


class Dispatch(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    text_message = models.TextField()
    client_filter = models.IntegerField(choices=ClientFilters.choices, null=True)
    client_filter_tag = models.CharField(max_length=100, blank=True, null=True)
    client_filter_mobile_operator_code = models.IntegerField(blank=True, null=True,
                                                             validators=[MinValueValidator(900),
                                                                         MaxValueValidator(997)])

    class Meta:
        ordering = ['start_time']
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_time__lt=models.F('end_time')),
                name='start_time_before_end_time'
            ),
            models.CheckConstraint(
                name='dispatch_client_filter_check',
                check=
                (models.Q(
                    client_filter=ClientFilters.TAG_FILTER,
                    client_filter_tag__isnull=False,
                    client_filter_mobile_operator_code__isnull=True) |
                 models.Q(
                     client_filter=ClientFilters.MOBILE_OPERATOR_CODE_FILTER,
                     client_filter_tag__isnull=True,
                     client_filter_mobile_operator_code__isnull=False)), )
        ]

    def send(self):
        from .tasks import send_message_to_client
        clients = []
        try:
            if 900 <= int(self.client_filter) <= 997:
                clients = Client.objects.filter(
                    mobile_operator_code=int(self.client_filter))
        except ValueError:
            clients = Client.objects.filter(tag__contains=self.client_filter)
        for client in clients:
            send_message_to_client.delay(self.id, client.id)


class Message(models.Model):
    STATUS_CHOICES = [
        ('S', 'Sent'),
        ('F', 'Failed'),
        ('P', 'Pending'),
    ]
    id = models.AutoField(primary_key=True)
    creation_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    dispatch = models.ForeignKey(Dispatch, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
