from django.contrib import admin
from users.models import User

class UserAdmin(admin.ModelAdmin):
    search_fields = ('user_role', 'phone_number')
    list_display = ('phone_number', 'user_role')

admin.site.register(User, UserAdmin)
# admin.site.register(UserConfirmation)
