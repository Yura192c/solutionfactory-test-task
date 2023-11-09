from datetime import datetime as time

from .models import Client, Dispatch, Message


def dispatch_create(*, start_time: time, end_time: time, text_message: str, client_filter) -> Dispatch:
    obj = Dispatch(
        start_time=start_time,
        end_time=end_time,
        text_message=text_message,
        client_filter=client_filter,
    )
    obj.full_clean()
    obj.save()
    return obj


def get_clients_list_in_dispatch(*, dispatch) -> list:
    if dispatch.client_filter == 1:
        return Client.objects.filter(tag__contains=dispatch.client_filter_tag)
    return Client.objects.filter(mobile_operator_code=dispatch.client_filter_mobile_operator_code)


def dispatch_send(*, dispatch):
    pass


def change_message_status(msg_id: int, stauts: str):
    message = Message.objects.get(id=msg_id)
    message.status = stauts
    message.full_clean()
    message.save()
