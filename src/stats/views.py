from django.shortcuts import render
from src.newsletter.models import Dispatch, Message, Client
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required


def clients_count(obj):
    clients = 0
    try:
        if 900 <= int(obj.client_filter) <= 997:
            clients = Client.objects.filter(mobile_operator_code=int(obj.client_filter))
    except:
        clients = Client.objects.filter(tag__contains=obj.client_filter)
    return clients.count()


def calculate_clients_count(monday):
    monday_clients_count = 0
    for obj in monday:
        monday_clients_count += clients_count(obj)
    return monday_clients_count


@login_required
def statistics(request):
    if request.user.is_superuser:
        current_date = timezone.now().date()

        # error_messages = messages.get_messages(request)
        # if error_messages:
        #     error_message = next(error_messages)

        current_week_day = current_date.weekday()
        # Вычисляем начало и конец недели
        start_of_week = current_date - timedelta(days=current_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        dispatches_this_week = Dispatch.objects.filter(start_time__range=(start_of_week, end_of_week))
        dispatches_this_week_count = dispatches_this_week.count()

        monday = dispatches_this_week.filter(start_time__week_day=2)
        monday_dispatches_count = monday.count()
        monday_clients_count = calculate_clients_count(monday)

        tuesday = dispatches_this_week.filter(start_time__week_day=3)
        tuesday_dispatches_count = tuesday.count()
        tuesday_clients_count = calculate_clients_count(tuesday)

        wednesday = dispatches_this_week.filter(start_time__week_day=4)
        wednesday_dispatches_count = wednesday.count()
        wednesday_clients_count = calculate_clients_count(wednesday)

        thursday = dispatches_this_week.filter(start_time__week_day=5)
        thursday_dispatches_count = thursday.count()
        thursday_clients_count = calculate_clients_count(thursday)

        friday = dispatches_this_week.filter(start_time__week_day=6)
        friday_dispatches_count = friday.count()
        friday_clients_count = calculate_clients_count(friday)

        saturday = dispatches_this_week.filter(start_time__week_day=7)
        saturday_dispatches_count = saturday.count()
        saturday_clients_count = calculate_clients_count(saturday)

        sunday = dispatches_this_week.filter(start_time__week_day=1)
        sunday_dispatches_count = sunday.count()
        sunday_clients_count = calculate_clients_count(sunday)

        # messages = Message.objects.filter()
        messages = Message.objects.filter(dispatch__in=dispatches_this_week)
        total_messages_count = messages.count()
        failed_messages = messages.filter(status='F')
        failed_messages_count = failed_messages.count()
        sent_messages = messages.filter(status='S')
        sent_messages_count = sent_messages.count()
        pending_messages = messages.filter(status='P')
        pending_messages_count = pending_messages.count()

        context = {
            'monday_dispatches_count': monday_dispatches_count,
            'monday_clients_count': monday_clients_count,
            'tuesday_dispatches_count': tuesday_dispatches_count,
            'tuesday_clients_count': tuesday_clients_count,
            'wednesday_dispatches_count': wednesday_dispatches_count,
            'wednesday_clients_count': wednesday_clients_count,
            'thursday_dispatches_count': thursday_dispatches_count,
            'thursday_clients_count': thursday_clients_count,
            'friday_dispatches_count': friday_dispatches_count,
            'friday_clients_count': friday_clients_count,
            'saturday_dispatches_count': saturday_dispatches_count,
            'saturday_clients_count': saturday_clients_count,
            'sunday_dispatches_count': sunday_dispatches_count,
            'sunday_clients_count': sunday_clients_count,

            'failed_messages_count': failed_messages_count,
            'sent_messages_count': sent_messages_count,
            'pending_messages_count': pending_messages_count,
            'total_messages_count': total_messages_count,

            'dispatches_this_week': dispatches_this_week,
            'dispatches_this_week_count': dispatches_this_week_count,
        }
        return render(request, 'stats/statistics.html', context)
    else:

        return render(request, 'stats/no_admin.html')
