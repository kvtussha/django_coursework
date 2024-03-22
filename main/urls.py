from django.urls import path

from main.views import SendingListView, SendingCreateView, SendingUpdateView, SendingDeleteView

app_name = 'main'

urlpatterns = [
    path('', SendingListView.as_view(), name='sending-list'),
    path('sending/detail/<int:pk>/', SendingListView.as_view(), name='sending-list'),
    path('sending/form/', SendingCreateView.as_view(), name='sending-form'),
    path('sending/edit/', SendingUpdateView.as_view(), name='sending-edit'),
    path('sending/delete/', SendingDeleteView.as_view(), name='sending-delete'),
]
