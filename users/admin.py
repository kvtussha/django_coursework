from django.contrib import admin

from users.models import User


@admin.register(User)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_verified', 'verification_code', )
    list_filter = ('email',)
