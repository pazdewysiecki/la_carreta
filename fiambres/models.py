from distutils.command.upload import upload
from pyexpat import model
from tabnanny import verbose
from django.db import models
from matplotlib import image
from matplotlib.style import available
from usuarios.models import Categoria_Usuario, Usuario
from django.utils.safestring import mark_safe


# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=300)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

class UnidadMedida(models.Model):
    id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'unidadmedida'
        verbose_name = 'unidadmedida'
        verbose_name_plural = 'unidadmedidas'
        ordering = ['id']

class Precios(models.Model):
    id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=300)
    tipo_usuario = models.ForeignKey(Categoria_Usuario, on_delete=models.CASCADE, default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'precios'
        verbose_name = 'Precio'
        verbose_name_plural = 'Precios'
        ordering = ['id']

class Product(models.Model):
    id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=300)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', blank =True)
    excerpt = models.TextField(max_length=200, verbose_name='Extracto')
    detail = models.TextField(max_length=1000, verbose_name='Información del producto')
    featured = models.BooleanField(default=False)
    #price_category = models.ForeignKey(Precios, on_delete=models.CASCADE)
    categoria_usuario = models.ForeignKey(Categoria_Usuario, on_delete=models.CASCADE,default=True)
    price = models.FloatField()
    available = models.BooleanField(default=True)
    unidadmedida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['id']

    def __str__(self):
        return self.name

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image))
    
 



class Order(models.Model):
    id = models.AutoField(primary_key= True)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    total_amt = models.FloatField()
    fecha_order = models.DateField(auto_now_add= True)
    estado_orden= models.BooleanField ('Iniciado', default=False)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        db_table = 'order'
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ['id']

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    items = models.CharField(max_length=150)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return str(self.order)
  
    def image_tag(self):
        return mark_safe('<img src="/media/products/%s" width="50" height="50" />' % (self.image))

    class Meta:
        db_table = 'orderitem'
        verbose_name = 'orderitem'
        verbose_name_plural = 'orderitems'
        ordering = ['id']
