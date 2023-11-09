from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from src.newsletter.models import ClientFilters, Dispatch


class DispatchTest(TestCase):
    def test_dispatch_end_time_cannot_before_start_date(self):
        dispatch_start_time = timezone.now()
        dispatch_end_time = timezone.now() - timedelta(days=1)

        dispatch = Dispatch(start_time=dispatch_start_time,
                            end_time=dispatch_end_time,
                            text_message='Test message',
                            client_filter=ClientFilters.TAG_FILTER,
                            client_filter_tag='test')

        with self.assertRaises(ValidationError):
            dispatch.full_clean()

    # def test_dispatch_client_filter_correct
