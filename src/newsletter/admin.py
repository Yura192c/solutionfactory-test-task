from django.contrib import admin
from .models import Client, Dispatch, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """ Клиенты
    """
    list_display = ('id', 'phone_number', 'mobile_operator_code', 'tag', 'timezone')


@admin.register(Dispatch)
class DispatchAdmin(admin.ModelAdmin):
    """ Рассылки
    """

    list_display = ('id', 'start_time', 'end_time', 'text_message', 'client_filter', 'clients_count')

    def clients_count(self, obj):
        clients = 0
        try:
            if 900 <= int(obj.client_filter) <= 997:
                clients = Client.objects.filter(mobile_operator_code=int(obj.client_filter))
        except:
            clients = Client.objects.filter(tag__contains=obj.client_filter)
        return clients.count()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """ Сообщения
    """
    list_display = ('id', 'creation_time', 'status', 'dispatch', 'client')
