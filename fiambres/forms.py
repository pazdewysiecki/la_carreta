
import imp
from django import forms


from .models import Order, OrderItems, Precios, Product, Category, UnidadMedida

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['estado_orden']
        labels = {
                'estado_orden': "Estado de orden:",
            }

    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug','category','excerpt', 'detail', 'price', 'image', 'available', 'unidadmedida','featured', 'categoria_usuario']
        labels = {
                'name': "Nombre del producto:",
                'category': "Categoría:",
                'unidadmedida': "Unidada de Medida",
                'slug': "Código del producto:",
                'excerpt': "Extracto:",
                'featured': "Producto en oferta",
                'detail': "Detalle:",
                'price':"Precio:",
                'image': "Imagen:",
                'available': "Producto disponible:",
                'categoria_usuario': "Listado de precio:",
                
            }
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el nombre del producto',
                    'id':'name'
                }
            ),
            'slug': forms.TextInput (
                 attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el código del producto',
                    'id':'slug'
                }
            ),
            'excerpt': forms.TextInput (
                 attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el extracto del producto',
                    'id':'excerpt'
                }
            ),
            'detail': forms.TextInput (
                 attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el detalle del producto',
                    'id':'detail'
                }
            ),
            'price': forms.TextInput (
                 attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el precio del producto',
                    'id':'price'
                }
            )
        }

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['featured', 'name','id']
        labels = {
                'name': "Nombre de la categoría:",
                'id': "Código de la categoría:",
                'featured': "Destacado:",
            }
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el nombre de la categoría',
                    'id':'name'
                }
            ),
        }

class UnidadaMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadMedida
        fields = ['name','id']
        labels = {
                'name': "Nombre de la unidad de medida:",
                'id': "Código de la unidad de medida:",
            }
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el nombre de la Unidad de Medida',
                    'id':'name'
                }
            ),
        }


class PreciosForm(forms.ModelForm):
    class Meta:
        model = Precios
        fields = ['name','id', 'tipo_usuario']
        labels = {
                'name': "Nombre del listado de precios:",
                'id': "Código del listado de precios:",
                'tipo_usuario': "Ingrese la categoría de Usuario"
            }
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el nombre del Listado de Precios',
                    'id':'name'
                }
            ),
        }

class PedidoForm(forms.ModelForm):
    class Meta:
        model = OrderItems
        fields = ['items', 'price','total','order', 'image', 'quantity']
        labels = {
                'items': "Nombre del producto:",
                'price': "Precio:",
                'total': "Total",
                'order': "order:",
                'image': "image:",
                'quantity': "quantity:",
            }
        widgets = {
            'items': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el nombre del producto',
                    'id':'items'
                }
            ),
            'price': forms.TextInput (
                 attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el código del producto',
                    'id':'price'
                }
            ),
            'total': forms.TextInput (
                 attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el extracto del producto',
                    'id':'total'
                }
            ),
            'order': forms.TextInput (
                 attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el detalle del producto',
                    'id':'order'
                }
            ),
            'quantity': forms.TextInput (
                 attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el precio del producto',
                    'id':'quantity'
                }
            ),
        }