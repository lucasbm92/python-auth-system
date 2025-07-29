from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'created_at', 'last_login')
    search_fields = ('email', 'username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'last_login')
