from django.contrib import admin
from domain.models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass
