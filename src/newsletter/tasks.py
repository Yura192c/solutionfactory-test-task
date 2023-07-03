from celery import shared_task
from src.newsletter.models import Dispatch, Client, Message
from config.settings.development import API_SENDING_URL, API_JWT_TOKEN
import requests


@shared_task
def send_message_to_client(dispatch_id, client_id):
    dispatch = Dispatch.objects.get(id=dispatch_id)
    client = Client.objects.get(id=client_id)

    url = f"{API_SENDING_URL}{client.id}"
    headers = {"Authorization": f"{API_JWT_TOKEN}"}
    data = {
        "id": client.id,
        "phone": client.phone_number,
        "text": dispatch.text_message,
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        print(response.status_code)
        if response.status_code == 200:
            message = Message.objects.create(
                status='S',
                dispatch=dispatch,
                client=client
            )
        elif response.status_code == 401:
            message = Message.objects.create(
                status='F',
                dispatch=dispatch,
                client=client
            )
        elif response.status_code == 400 or response.elapsed.total_seconds() > 10:
            # Повторная попытка отправки
            try:
                response_retry = requests.post(url, headers=headers, json=data)
                if response_retry.status_code == 200:
                    message = Message.objects.create(
                        status='S',
                        dispatch=dispatch,
                        client=client
                    )
                else:
                    message = Message.objects.create(
                        status='F',
                        dispatch=dispatch,
                        client=client
                    )
            except requests.exceptions.RequestException:
                message = Message.objects.create(
                    status='F',
                    dispatch=dispatch,
                    client=client
                )
        else:
            message = Message.objects.create(
                status='F',
                dispatch=dispatch,
                client=client
            )
    except requests.exceptions.RequestException:
        message = Message.objects.create(
            status='F',
            dispatch=dispatch,
            client=client
        )
    except Exception as e:
        message = Message.objects.create(
            status='F',
            dispatch=dispatch,
            client=client
        )
        # Обработка ошибки при выполнении запроса
        print(f"An error occurred: {str(e)}")
