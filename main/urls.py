from django.urls import path

from main.views import (MailingListView, MailingCreateView,
                        MailingUpdateView, MailingDeleteView, contacts)

app_name = 'main'

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing-list'),
    path('contacts/', contacts, name='contacts'),
    path('mailing/detail/<int:pk>/', MailingListView.as_view(), name='mailing-detail'),
    path('mailing/form/', MailingCreateView.as_view(), name='mailing-form'),
    path('mailing/edit/', MailingUpdateView.as_view(), name='mailing-edit'),
    path('mailing/delete/', MailingDeleteView.as_view(), name='mailing-delete'),
]
