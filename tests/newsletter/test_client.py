from django.core.exceptions import ValidationError
from django.test import TestCase

from src.newsletter.models import Client


class ClientModelTestCase(TestCase):
    def test_valid_client(self):
        # Проверяем, что создание клиента с правильными данными не вызывает ошибок
        client = Client(
            phone_number='79999999999',
            mobile_operator_code=900,
            tag='Test Client',
            timezone='Europe/Moscow',
        )
        client.full_clean()  # Убедитесь, что модель проходит валидацию
        client.save()
        self.assertEqual(Client.objects.count(), 1)

    def test_invalid_phone_number(self):
        # Проверяем, что недопустимый номер телефона вызывает ошибку валидации
        with self.assertRaises(ValidationError):
            client = Client(
                phone_number='1234567890',  # Недопустимый номер телефона
                mobile_operator_code=900,
                tag='Test Client',
                timezone='Europe/Moscow',
            )
            client.full_clean()

    def test_invalid_mobile_operator_code(self):
        # Проверяем, что недопустимый код оператора вызывает ошибку валидации
        with self.assertRaises(ValidationError):
            client = Client(
                phone_number='79999999999',
                mobile_operator_code=800,  # Недопустимый код оператора
                tag='Test Client',
                timezone='Europe/Moscow',
            )
            client.full_clean()

    def test_valid_mobile_operator_code(self):
        # Проверяем, что допустимый код оператора не вызывает ошибки валидации
        client = Client(
            phone_number='79999999999',
            mobile_operator_code=900,  # Допустимый код оператора
            tag='Test Client',
            timezone='Europe/Moscow',
        )
        client.full_clean()
        client.save()
        self.assertEqual(Client.objects.count(), 1)

