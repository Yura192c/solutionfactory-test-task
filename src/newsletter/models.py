from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils import timezone


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^7[0-9]{10}$',
                message='Phone number must be in the format 7XXXXXXXXXX',
            ),
        ],
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
                name='start_time_before_end_time',
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
                     client_filter_mobile_operator_code__isnull=False))),
        ]

    def send(self):
        from .tasks import send_message_to_client
        from .services import get_clients_list_in_dispatch
        clients = get_clients_list_in_dispatch(dispatch=self)
        for client in clients:
            send_message_to_client.delay(self.id, client.id)


class MessageStatus(models.TextChoices):
    SENT = 'S', 'Sent'
    FAILED = 'F', 'Failed'
    PENDING = 'P', 'Pending'


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=255, db_index=True, choices=MessageStatus.choices,
                              default=MessageStatus.PENDING)
    dispatch = models.ForeignKey(Dispatch, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    creation_time = models.DateTimeField(default=timezone.now)
    sending_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['creation_time', 'sending_time']
        constraints = [
            models.CheckConstraint(
                name='sending_time_with_status_sent',
                check=models.Q(status=MessageStatus.SENT) | models.Q(sending_time__isnull=True),
            ),
        ]
