from django.utils import timezone

from rest_framework import serializers

from .models import Client, Dispatch, Message
from .services import get_clients_list_in_dispatch


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class DispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch
        fields = ('id', 'start_time', 'end_time', 'text_message', 'client_filter',
                  'client_filter_tag', 'client_filter_mobile_operator_code')


class DispatchStatsSerializer(serializers.ModelSerializer):
    clients = serializers.SerializerMethodField()
    successful_messages = serializers.SerializerMethodField()
    failed_messages = serializers.SerializerMethodField()
    errors = serializers.SerializerMethodField()
    pending = serializers.SerializerMethodField()

    class Meta:
        model = Dispatch
        # fields = ('id', 'clients', 'successful_messages', 'failed_messages',
        #           'pending', 'errors', 'text_message')
        fields = '__all__'

    def get_clients(self, instance):
        # Логика для получения списка клиентов в рассылке
        clients = get_clients_list_in_dispatch()
        return ClientSerializer(clients, many=True).data

    def get_successful_messages(self, instance):
        # Логика для получения количества успешных сообщений
        successful_messages = instance.message_set.filter(status='S').count()
        return successful_messages

    def get_failed_messages(self, instance):
        # Логика для получения количества неуспешных сообщений
        failed_messages = instance.message_set.filter(status='F').count()
        return failed_messages

    def get_errors(self, instance):
        # Логика для получения количества ошибок
        errors = instance.message_set.filter(status='E').count()
        return errors

    def get_message_text(self, instance):
        # Логика для получения текста сообщения
        message = Message.objects.filter(dispatch=instance).first()
        return message.text_message if message else ''

    def get_pending(self, instance):
        current_time = timezone.now()
        return current_time < instance.start_time


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
