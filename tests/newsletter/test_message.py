from django.core.exceptions import ValidationError
from django.test import TestCase

from src.newsletter.models import Client, ClientFilters, Dispatch, Message, MessageStatus


class MessageModelTestCase(TestCase):
    def setUp(self):
        # Создаем объекты Dispatch и Client для связывания с сообщениями
        self.dispatch = Dispatch.objects.create(
            start_time='2023-11-08 10:00:00',
            end_time='2023-11-08 12:00:00',
            text_message='Test message',
            client_filter=ClientFilters.TAG_FILTER,
            client_filter_tag='Test Tag'
        )
        self.client = Client.objects.create(
            phone_number='79999999999',
            mobile_operator_code=900,
            tag='Test Client',
            timezone='Europe/Moscow'
        )

    def test_valid_message(self):
        # Проверяем, что создание сообщения с правильными данными не вызывает ошибок
        message = Message(
            status=MessageStatus.SENT,
            dispatch=self.dispatch,
            client=self.client,
            creation_time='2023-11-08 10:30:00',
            sending_time='2023-11-08 10:45:00'
        )
        message.full_clean()  # Убедитесь, что модель проходит валидацию
        message.save()
        self.assertEqual(Message.objects.count(), 1)

    def test_invalid_status(self):
        # Проверяем, что недопустимый статус вызывает ошибку валидации
        with self.assertRaises(ValidationError):
            message = Message(
                status='InvalidStatus',  # Недопустимый статус
                dispatch=self.dispatch,
                client=self.client,
                creation_time='2023-11-08 10:30:00',
                sending_time='2023-11-08 10:45:00'
            )
            message.full_clean()

    def test_invalid_sending_time_without_status_sent(self):
        # Проверяем, что если статус не 'Sent', отправочное время должно быть пустым
        with self.assertRaises(ValidationError):
            message = Message(
                status=MessageStatus.PENDING,
                dispatch=self.dispatch,
                client=self.client,
                creation_time='2023-11-08 10:30:00',
                sending_time='2023-11-08 10:45:00'
            )
            message.full_clean()

    def test_valid_sending_time_with_status_sent(self):
        # Проверяем, что отправочное время с правильным статусом 'Sent' не вызывает ошибки валидации
        message = Message(
            status=MessageStatus.SENT,
            dispatch=self.dispatch,
            client=self.client,
            creation_time='2023-11-08 10:30:00',
            sending_time='2023-11-08 10:45:00'
        )
        message.full_clean()
        message.save()
        self.assertEqual(Message.objects.count(), 1)

