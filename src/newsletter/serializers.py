from django.utils import timezone
from rest_framework import serializers
from .models import Message, Dispatch, Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class DispatchSerializer(serializers.ModelSerializer):
    # clients = serializers.SerializerMethodField()

    class Meta:
        model = Dispatch
        # fields = '__all__'
        fields = ('id', 'start_time', 'end_time', 'text_message', 'client_filter')

    # def get_clients(self, instance):
    #     # Логика для получения списка клиентов в рассылке
    #     clients = []
    #     try:
    #         if 990 <= int(instance.client_filter) <= 997:
    #             clients = Client.objects.filter(mobile_operator_code=int(instance.client_filter))
    #     except ValueError:
    #         clients = Client.objects.filter(tag__contains=instance.client_filter)
    #     return ClientSerializer(clients, many=True).data


class DispatchStatsSerializer(serializers.ModelSerializer):
    clients = serializers.SerializerMethodField()
    successful_messages = serializers.SerializerMethodField()
    failed_messages = serializers.SerializerMethodField()
    errors = serializers.SerializerMethodField()
    pending = serializers.SerializerMethodField()

    class Meta:
        model = Dispatch
        fields = ('id', 'clients', 'successful_messages', 'failed_messages',
                  'pending', 'errors', 'text_message')

    def get_clients(self, instance):
        # Логика для получения списка клиентов в рассылке
        clients = []
        try:
            if 900 <= int(instance.client_filter) <= 997:
                clients = Client.objects.filter(mobile_operator_code=int(instance.client_filter))
        except ValueError:
            clients = Client.objects.filter(tag__contains=instance.client_filter)
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

    def get_pending(selfself, instance):
        current_time = timezone.now()
        return current_time < instance.start_time


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
