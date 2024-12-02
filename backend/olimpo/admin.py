from django.contrib import admin
from olimpo.models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'cedula', 'telefono', 'nombres', 'apellidos', 'activo']
admin.site.register(User, UserAdmin)

class ClienteAdmin(admin.ModelAdmin):
    list_display = ['cedula', 'nombres', 'apellidos', 'telefono', 'activo']
admin.site.register(Cliente, ClienteAdmin)