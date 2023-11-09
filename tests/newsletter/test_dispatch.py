from django.core.exceptions import ValidationError
from django.test import TestCase

from src.newsletter.models import ClientFilters, Dispatch


class DispatchModelTestCase(TestCase):
    def test_valid_dispatch(self):
        # Проверяем, что создание рассылки с правильными данными не вызывает ошибок
        dispatch = Dispatch(
            start_time='2023-11-08 10:00:00',
            end_time='2023-11-08 12:00:00',
            text_message='Test message',
            client_filter=ClientFilters.TAG_FILTER,
            client_filter_tag='Test Tag',
        )
        dispatch.full_clean()  # Убедитесь, что модель проходит валидацию
        dispatch.save()
        self.assertEqual(Dispatch.objects.count(), 1)

    def test_invalid_start_time_before_end_time(self):
        # Проверяем, что неправильное время начала и окончания вызывает ошибку валидации
        with self.assertRaises(ValidationError):
            dispatch = Dispatch(
                start_time='2023-11-08 14:00:00',  # Окончание перед началом
                end_time='2023-11-08 12:00:00',
                text_message='Test message',
                client_filter=ClientFilters.TAG_FILTER,
                client_filter_tag='Test Tag',
            )
            dispatch.full_clean()

    def test_invalid_client_filter_combination(self):
        # Проверяем, что неправильные комбинации фильтров клиентов вызывают ошибку валидации
        with self.assertRaises(ValidationError):
            dispatch = Dispatch(
                start_time='2023-11-08 10:00:00',
                end_time='2023-11-08 12:00:00',
                text_message='Test message',
                client_filter=ClientFilters.MOBILE_OPERATOR_CODE_FILTER,
                client_filter_tag='Test Tag',  # Недопустимая комбинация фильтров
            )
            dispatch.full_clean()

    def test_valid_mobile_operator_code(self):
        # Проверяем, что допустимый код оператора не вызывает ошибки валидации
        dispatch = Dispatch(
            start_time='2023-11-08 10:00:00',
            end_time='2023-11-08 12:00:00',
            text_message='Test message',
            client_filter=ClientFilters.MOBILE_OPERATOR_CODE_FILTER,
            client_filter_mobile_operator_code=900,
        )
        dispatch.full_clean()
        dispatch.save()
        self.assertEqual(Dispatch.objects.count(), 1)
