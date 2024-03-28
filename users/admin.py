from django.contrib import admin

from users.models import User


@admin.register(User)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'verification_code', 'is_password_reset',
                    'is_active', 'is_staff')
    list_filter = ('email',)
