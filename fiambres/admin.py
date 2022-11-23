from http.client import ImproperConnectionState
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from usuarios.models import Usuario
from .models import Category, Product, Order, OrderItems
# Register your models here.


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class ProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ('id', 'name', 'slug','category__name', 'image', 'excerpt', 'detail', 'featured','price', 'available', 'categoria_usuario__name','unidadmedida__name')
    list_display= ('id', 'name', 'slug', 'category', 'image', 'excerpt', 'detail', 'featured', 'categoria_usuario', 'price', 'available', 'unidadmedida')
    resource_class = ProductResource
    class Meta:
        model = Product
    

admin.site.register ([Category, Order, OrderItems])
admin.site.register(Product, ProductAdmin)

