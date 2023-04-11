from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from chat.models import Chat, Contact
from chat.views import get_user_contact
from .serializers import ChatSerializer

User = get_user_model()


class ChatListView(ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        queryset = Chat.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            contact = get_user_contact(username)
            queryset = contact.chats.all()
        return queryset


class ChatDetailView(RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.AllowAny, )


class ChatCreateView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChatUpdateView(UpdateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ChatDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )



from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from chat.models import Chat, Contact
from chat.api.serializers import ChatSerializer
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Count

User = get_user_model()


@api_view(['POST'])
def get_or_create_chat(request, user1_id, user2_id):
    user1 = get_object_or_404(Contact, user_id=user1_id)
    user2 = get_object_or_404(Contact, user_id=user2_id)
    chat = Chat.objects.annotate(num_participants=Count('participants')).filter(num_participants=2, participants=user1).filter(participants=user2)

    if chat:
        chat = chat.first()

    else:
        chat = Chat.objects.create()
        chat.participants.add(user1)
        chat.participants.add(user2)
        chat.save()

    messages = list(chat.messages.all().values('content', 'timestamp'))
    data = {
        'id': chat.id,
        'participants': [user1.user.username, user2.user.username],
        'messages': messages
    }
    return JsonResponse(data, safe=False)
