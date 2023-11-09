from django.contrib import admin

from .models import Client, Dispatch, Message
from .services import get_clients_list_in_dispatch


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """ Клиенты
    """
    list_display = ('id', 'phone_number', 'mobile_operator_code', 'tag', 'timezone')


@admin.register(Dispatch)
class DispatchAdmin(admin.ModelAdmin):
    """ Рассылки
    """

    list_display = ('id', 'start_time', 'end_time', 'text_message', 'client_filter', 'client_filter_tag',
                    'client_filter_mobile_operator_code', 'get_clients_count')

    fieldsets = (
        ('Base Information', {
            'fields': ('start_time', 'end_time', 'text_message', 'client_filter', 'client_filter_tag',
                       'client_filter_mobile_operator_code'),
        }),
    )

    def get_clients_count(self, obj):
        return get_clients_list_in_dispatch(dispatch=obj).count()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """ Сообщения
    """
    list_display = ('id', 'status', 'dispatch', 'client', 'creation_time', 'sending_time')
