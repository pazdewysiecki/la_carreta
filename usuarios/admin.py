from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from usuarios.models import Usuario



class UsuarioResource(resources.ModelResource):
    class Meta:
        model = Usuario

class UsuarioAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ('id', 'username', 'nombre','direccion','tipo_usuario__name', 'is_active', 'is_staff')
    list_display= ('id', 'username', 'nombre','direccion', 'tipo_usuario', 'is_active', 'is_staff')
    resource_class = UsuarioResource
    class Meta:
        model = Usuario

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Permission)
admin.site.register(ContentType)

