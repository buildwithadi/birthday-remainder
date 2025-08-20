from django.contrib import admin
from .models import User, Contact, EmailReminder

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','date_of_birth', 'user',)
    search_fields = ('name',)

@admin.register(EmailReminder)
class EmailReminderAdmin(admin.ModelAdmin):
    list_display = ('contact', 'sent_at')
    list_filter = ('sent_at',)