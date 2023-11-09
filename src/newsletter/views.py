from datetime import timedelta

from rest_framework import generics, permissions

from src.base.classes import CreateRetrieveUpdateDestroy as CRUD
from src.newsletter.tasks import send_message_to_client

from .models import Client, Dispatch, Message
from .serializers import ClientSerializer, DispatchSerializer, DispatchStatsSerializer, MessageSerializer
from .services import get_clients_list_in_dispatch


class ClientView(CRUD):
    """ CRUD client """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes_by_action = {'create': [permissions.AllowAny],
                                    'list': [permissions.IsAdminUser],
                                    'retrieve': [permissions.IsAdminUser],
                                    'update': [permissions.IsAdminUser],
                                    'destroy': [permissions.IsAdminUser]}


class DispatchView(CRUD):
    """ CRUD dispatch """
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer
    permission_classes_by_action = {'create': [permissions.IsAuthenticated],
                                    'list': [permissions.IsAdminUser],
                                    'retrieve': [permissions.IsAdminUser],
                                    'update': [permissions.IsAdminUser],
                                    'destroy': [permissions.IsAdminUser]}

    def perform_create(self, serializer):
        serializer.save()
        dispatch = serializer.instance

        dispatch_time = dispatch.start_time
        eta = dispatch_time - timedelta(hours=3)

        clients = get_clients_list_in_dispatch(dispatch=dispatch)

        for client in clients:
            send_message_to_client.apply_async(args=[dispatch.id, client.id],
                                               eta=eta)


class DispatchStatsView(generics.RetrieveAPIView):
    """ Get stats for a specific dispatch """
    queryset = Dispatch.objects.all()
    serializer_class = DispatchStatsSerializer
    permission_classes = [permissions.IsAdminUser]


class MessageView(generics.ListAPIView):
    """ List messages for a specific dispatch """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        dispatch_id = self.kwargs['dispatch_id']
        return Message.objects.filter(dispatch_id=dispatch_id)
