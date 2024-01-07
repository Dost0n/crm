from django.contrib import admin
from clients.models import Client, ClientConfirmation, File, Graphic



class ClientAdmin(admin.ModelAdmin):
    search_fields = ('phone_number', 'fullname')
    list_display = ('fullname', 'passport', 'pinfl')


admin.site.register(Client, ClientAdmin)
admin.site.register(ClientConfirmation)
admin.site.register(File)
admin.site.register(Graphic)
