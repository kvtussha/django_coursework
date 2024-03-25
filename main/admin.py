from django.contrib import admin

from main.models import Client, Message, Sending, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'comment', 'is_active')
    list_filter = ('name', 'comment', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'subject', 'body', )
    list_filter = ('created_at', 'subject', 'body')


@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
    list_display = ('scheduled_time', 'status', 'message', 'start_date', 'end_date',
                    'frequency')
    list_filter = ('scheduled_time', 'start_date', 'message')


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('sending', 'sent_at', 'status', 'response', )
    list_filter = ('sent_at', 'status', )

