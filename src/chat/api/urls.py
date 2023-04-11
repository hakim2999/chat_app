from django.urls import path, re_path

from .views import (
    ChatListView,
    ChatDetailView,
    ChatCreateView,
    ChatUpdateView,
    ChatDeleteView
)
from .views import get_or_create_chat
app_name = 'chat'

urlpatterns = [
    path('', ChatListView.as_view()),
    path('create/', ChatCreateView.as_view()),
    path('<pk>', ChatDetailView.as_view()),
    path('<pk>/update/', ChatUpdateView.as_view()),
    path('<pk>/delete/', ChatDeleteView.as_view()),
    path('<int:user1_id>/<int:user2_id>/', get_or_create_chat, name='get_or_create_chat'),
   
]
