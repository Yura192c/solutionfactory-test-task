from rest_framework import generics, permissions
from .models import Message, Dispatch, Client
from .serializers import MessageSerializer, DispatchSerializer, ClientSerializer, DispatchStatsSerializer
from src.base.classes import CreateRetrieveUpdateDestroy as CRUD
from src.newsletter.tasks import send_message_to_client
from datetime import timedelta


class ClientView(CRUD):
    ''' CRUD client '''
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes_by_action = {'create': [permissions.AllowAny],
                                    'list': [permissions.IsAdminUser],
                                    'retrieve': [permissions.IsAdminUser],
                                    'update': [permissions.IsAdminUser],
                                    'destroy': [permissions.IsAdminUser]}


class DispatchView(CRUD):
    ''' CRUD dispatch '''
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer
    permission_classes_by_action = {'create': [permissions.IsAdminUser],
                                    'list': [permissions.IsAdminUser],
                                    'retrieve': [permissions.IsAdminUser],
                                    'update': [permissions.IsAdminUser],
                                    'destroy': [permissions.IsAdminUser]}

    def perform_create(self, serializer):
        serializer.save()
        dispatch = serializer.instance

        dispatch_time = dispatch.start_time
        eta = dispatch_time - timedelta(hours=3)

        clients = []
        try:
            if 900 <= int(dispatch.client_filter) <= 997:
                clients = Client.objects.filter(mobile_operator_code=int(dispatch.client_filter))
        except ValueError:
            clients = Client.objects.filter(tag__contains=dispatch.client_filter)

        for client in clients:
            send_message_to_client.apply_async(args=[dispatch.id, client.id],
                                               eta=eta)


class DispatchStatsView(generics.RetrieveAPIView):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchStatsSerializer


class MessageView(generics.ListAPIView):
    ''' List messages for a specific dispatch '''
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        dispatch_id = self.kwargs['dispatch_id']
        return Message.objects.filter(dispatch_id=dispatch_id)

    def post(self, request, *args, **kwargs):
        dispatch_id = self.kwargs['dispatch_id']
        dispatch = Dispatch.objects.get(id=dispatch_id)
        dispatch.send()
        return self.list(request, *args, **kwargs)
