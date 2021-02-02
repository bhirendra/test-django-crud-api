from django.contrib import admin
from main.models import UserData


class UserDataAdmin(admin.ModelAdmin):
    """
    Admin config setting of user data table
    """
    date_hierarchy = 'created'
    list_display = ['id', 'user', 'email', 'mobile', 'created', 'modified']
    list_filter = ['user']
    search_fields = ['user__username', 'email', 'mobile']
    autocomplete_fields = (('user'),)


admin.site.register(UserData, UserDataAdmin)
