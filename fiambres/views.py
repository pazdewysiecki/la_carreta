from email import message
from pyexpat import features
from urllib import response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from numpy import product

from fiambres import cart
from fiambres.forms import OrderForm, PedidoForm, PreciosForm, ProductForm, CategoryForm, UnidadaMedidaForm
from .models import Category, Order, Product, OrderItems, UnidadMedida, Precios
from ast import Try
from http import client
from multiprocessing import context
from pydoc import cli
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import View, generic
from django.views.generic import TemplateView,ListView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy 
from django.http import HttpResponse
from requests import request
from django.core.paginator import Paginator
from jsignature.utils import draw_signature
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.core.exceptions import ValidationError
from django import forms
from usuarios.models import Categoria_Usuario, Usuario
from django.contrib.auth.decorators import permission_required
from usuarios.mixins import ValidarPermisosRequeridosMixin
from fiambres.cart import *
import mercadopago


#Clase para inciar#

class Inicio(TemplateView):
    template_name = 'index.html'

class InicioSistema(TemplateView):
    template_name = 'fiambres/listado_productos.html'

class Meta:
        ordering = ('date',)


def listado_productos(request):
        busqueda = request.GET.get("buscar")
        cat=Categoria_Usuario.objects.all()
        #usuarios = Usuario.objects.filter(tipo_usuario = cat)
        #categoria_precio = Precios.objects.filter(tipo_usuario = request.tipo_usuario)
        products = Product.objects.filter(available=True, categoria_usuario=request.user.tipo_usuario)
        categories = Category.objects.all()
        #paginator = Paginator(products, 20)
        #page_number = request.GET.get('page')
        #page_obj = paginator.get_page(page_number)

        if busqueda:
            products = Product.objects.filter(
                Q (name__icontains = busqueda) |
                Q (category__name__icontains = busqueda) |
                Q (price__icontains = busqueda)
            ).distinct()
            return render(request, 'fiambres/listado_productos.html', {'products':products, 'categories': categories, 'cat':cat})
        else:
            return render(request, 'fiambres/listado_productos.html', {'products': products, 'categories': categories, 'cat':cat})

def buscar_categoriass(request,id):
    busqueda = request.GET.get("buscar")
    template_name='fiambres/listado_productos.html'
    cat=Category.objects.get(id=id)
    categories = Category.objects.all()
    products = Product.objects.filter(available=True, category=cat)
    context = {"products":products, "categories":categories}

    if busqueda:
            products = Product.objects.filter(
                Q (name__icontains = busqueda) |
                Q (category__name__icontains = busqueda) |
                Q (price__icontains = busqueda)
            ).distinct()
            return render(request, 'fiambres/listado_productos.html', {'products':products, 'categories': categories})
    else:
            return render(request, 'fiambres/listado_productos.html', context)

    

def detail(request,slug):
    if Product.objects.filter(available=True, slug=slug).exists():
        template_name = 'fiambres/detail.html'
        products = Product.objects.filter(available=True, slug=slug)
        categories = Category.objects.all()
        context = {"products":products, "categories":categories}
        return render(request, template_name, context)

def add_product(request, product_id):
    carrito = Cart(request)
    product = Product.objects.get(id=product_id)
    carrito.add(product)
    return redirect('fiambres:listado_productos')
    
def remove_product(request, product_id):
    carrito = Cart(request)
    product = Product.objects.get(id=product_id)
    carrito.remove(product)
    return redirect('fiambres:listado_productos')

def decrement_product(request, product_id):
    carrito = Cart(request)
    product = Product.objects.get(id=product_id)
    carrito.decrement(product)
    return redirect('fiambres:listado_productos')

def clean_product(request):
    carrito = Cart(request)
    carrito.clear()
    return redirect('fiambres:listado_productos')

class ListadoPedidos(generic.ListView):
    template_name = 'fiambres/listado_pedidos.html'
    context_object_name = 'products'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ListadoPedidos, self).get_context_data(**kwargs)
        context.update({
            'products': Product.objects.all(),
            'categories': Category.objects.all(),
        })
        return context

    def get_queryset(self):
        return Product.objects.all()

class CrearOrden(CreateView):
    form_class = OrderForm
    template_name = 'fiambres/checkout.html'
    success_url = reverse_lazy ('fiambres/listado_productos.html')
        
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            cart_id = self.request.session.get("cart", None)
            if cart_id:
                cart_obj = Cart.objects.get(id=cart_id)
            else:
                cart_obj= None
                context['cart'] = cart_obj
                return context

    def form_valid(self, form):
        cart_id= self.request.session.get(id=cart_id)
        if cart_id:
                cart_obj = Cart.objects.get(id=cart_id)
                form.instance.cart = cart_obj
                form.instance.value.name = cart_obj.total_amt
                form.instance.session = cart_obj.user 
        else:
            return redirect('fiambres/listado_productos.html') 
        return super().form_valid(form)
    
def checkout(request):
    total_amt=0
    if 'cart' in request.session:
        for key, value in request.session["cart"].items():
            total_amt+= float(value["price"])

        order=Order.objects.create(
            user=request.user,
            total_amt=total_amt
        )

        for key, value in request.session["cart"].items():
            total_amt+= float(value["price"])

            items=OrderItems.objects.create(
                order=order,
                items=value['name'],
                image= value['image'],
                quantity=value['quantity'],
                price=value['price'],
                total= float(value["price"])* float(value["quantity"])
            )
        """
        for key, value in request.session["cart"].items():
            total_amt+= float(value["price"])

            items=Product.objects.update(
                id = value['product.id'],
                cantidad= (value['cantidad'] - value['quantity'])
            )
        """

        sdk = mercadopago.SDK("APP_USR-1953709056975791-070715-dbf32f00aac6e14906d2c359d9da757a-127856537")
        preference_data = {
            "items": [
                {
                    "title": "Mis productos",
                    "quantity": 1,
                    "unit_price": (total_amt/2),
                }
            ]
        }
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        print(preference_data, preference)
    return render(request,'fiambres/checkout.html', {'cart':request.session['cart'], 'total':len(request.session['cart']), 'total_amt':total_amt, 'preference': preference})

def pagar(request):
    sdk = mercadopago.SDK("APP_USR-1953709056975791-070715-dbf32f00aac6e14906d2c359d9da757a-127856537")

    preference_data = {
        "items": [
            {
                "title": "Mis productos",
                "quantity": 1,
                "unit_price": 22,
            }
        ]
    }
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    print(preference_data, preference)
    return render(request,'fiambres/pago2.html', {'preference': preference})



#Productos


class ListarProductos(ValidarPermisosRequeridosMixin,ListView):
    model = Product
    template_name = 'fiambres/listar_productos.html'
    permission_required = ('fiambres.view_productos','fiambres.add_productos','fiambres.delete_productos','fiambres.change_productos')
    context_object_name = 'productos'
    queryset = Product.objects.all()
    paginate_by = 1


class EditarProductos(ValidarPermisosRequeridosMixin,UpdateView):
    model = Product
    template_name = 'fiambres/modalProductos.html'
    permission_required = ('fiambres.view_productos','fiambres.add_productos','fiambres.delete_productos','fiambres.change_productos')
    form_class = ProductForm
    success_url = reverse_lazy ('fiambres:listar_productos')


class CrearProductos(ValidarPermisosRequeridosMixin,CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'fiambres/crear_productos.html'
    permission_required = ('fiambres.view_productos','fiambres.add_productos','fiambres.delete_productos','fiambres.change_productos')
    success_url = reverse_lazy ('fiambres:listar_productos')

class CrearModalProductos(ValidarPermisosRequeridosMixin,CreateView):
    model = Product
    template_name = 'fiambres/modalcrearproductos.html'
    permission_required = ('fiambres.view_productos','fiambres.add_productos','fiambres.delete_productos','fiambres.change_productos')
    form_class = ProductForm
    success_url = reverse_lazy ('fiambres:listar_productos')
    

class EliminarProductos(ValidarPermisosRequeridosMixin,DeleteView):
    model = Product
    permission_required = ('fiambres.view_productos','fiambres.add_productos','fiambres.delete_productos','fiambres.change_productos')
    success_url = reverse_lazy ('fiambres:listar_productos')

@permission_required('fiambres.view_productos',login_url='home')
@permission_required('fiambres.add_productos',login_url='home')
@permission_required('fiambres.delete_productos',login_url='home')
@permission_required('fiambres.change_productos',login_url='home')
def buscar_productos(request):
        busqueda = request.GET.get("buscar")
        products = Product.objects.all().order_by('-id')
        paginator = Paginator(products, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if busqueda:
                products = Product.objects.filter(
                    Q (name__icontains = busqueda) |
                    Q (slug__icontains= busqueda) |
                    Q (category__name__icontains= busqueda) |
                    Q (price__icontains= busqueda) 
                ).distinct()
                return render(request, 'fiambres/listar_productos.html', {'products':products})
        else:
            return render(request, 'fiambres/listar_productos.html', {'products': page_obj})

#Categorías


class ListarCategorias(ValidarPermisosRequeridosMixin,ListView):
    model = Category
    template_name = 'fiambres/listar_categorias.html'
    permission_required = ('fiambres.view_categorias','fiambres.add_categorias','fiambres.delete_categorias','fiambres.change_categorias')
    context_object_name = 'categorias'
    queryset = Category.objects.all()
    paginate_by = 1


class EditarCategorias(ValidarPermisosRequeridosMixin,UpdateView):
    model = Category
    template_name = 'fiambres/modalCategorias.html'
    permission_required = ('fiambres.view_categorias','fiambres.add_categorias','fiambres.delete_categorias','fiambres.change_categorias')
    form_class = CategoryForm
    success_url = reverse_lazy ('fiambres:listar_categorias')


class CrearCategorias(ValidarPermisosRequeridosMixin,CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'fiambres/crear_categorias.html'
    permission_required = ('fiambres.view_categorias','fiambres.add_categorias','fiambres.delete_categorias','fiambres.change_categorias')
    success_url = reverse_lazy ('fiambres:listar_categorias')

class CrearModalCategorias(ValidarPermisosRequeridosMixin,CreateView):
    model = Category
    template_name = 'fiambres/modalcrearcategorias.html'
    permission_required = ('fiambres.view_categorias','fiambres.add_categorias','fiambres.delete_categorias','fiambres.change_categorias')
    form_class = CategoryForm
    success_url = reverse_lazy ('fiambres:listar_categorias')
    

class EliminarCategorias(ValidarPermisosRequeridosMixin,DeleteView):
    model = Category
    permission_required = ('fiambres.view_categorias','fiambres.add_categorias','fiambres.delete_categorias','fiambres.change_categorias')
    success_url = reverse_lazy ('fiambres:listar_categorias')

@permission_required('fiambres.view_categorias',login_url='home')
@permission_required('fiambres.add_categorias',login_url='home')
@permission_required('fiambres.delete_categorias',login_url='home')
@permission_required('fiambres.change_categorias',login_url='home')
def buscar_categorias(request):
        busqueda = request.GET.get("buscar")
        categories = Category.objects.all().order_by('-id')
        paginator = Paginator(categories, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if busqueda:
                categories = Category.objects.filter(
                    Q (name__icontains = busqueda) |
                    Q (id__icontains= busqueda)
                ).distinct()
                return render(request, 'fiambres/listar_categorias.html', {'categories':categories})
        else:
            return render(request, 'fiambres/listar_categorias.html', {'categories': page_obj})


def buscar_usuarios_ordenes(request):
        ordenes_usuarios = Order.objects.filter(user = request.user).filter(estado_orden=False).order_by('-id')
        context = {'ordenes_usuarios':ordenes_usuarios}
        return render(request, 'fiambres/listar_ordenes_usuario.html', context)


def buscar_usuarios_ordenes_id(request,id):
    orden_usuario=Order.objects.filter(id=id).filter(user=request.user).first()
    orderitems = OrderItems.objects.filter(order=orden_usuario)
    context = {'orden_usuario':orden_usuario, 'orderitems':orderitems}
    return render(request, 'fiambres/listar_ordenes_usuario_id.html', context)

def buscar_usuarios_ordenes_historico(request):
        ordenes_usuarios = Order.objects.filter(user = request.user).order_by('-id')
        context = {'ordenes_usuarios':ordenes_usuarios}
        return render(request, 'fiambres/listar_ordenes_historico.html', context)

    
    
class VerPedido(UpdateView):
    model = Order
    template_name = 'fiambres/modalOrden.html'
    #permission_required = ('fiambres.view_categorias','fiambres.add_categorias','fiambres.delete_categorias','fiambres.change_categorias')
    form_class = OrderForm
    success_url = reverse_lazy ('fiambres:pedido_historico')

def buscar_pedido(request):
        ordenes_usuarios = Order.objects.filter(estado_orden=False).order_by('-id')
        context = {'ordenes_usuarios':ordenes_usuarios}
        return render(request, 'fiambres/pedido_historico.html', context)

def buscar_pedido_id(request,id):
    orden_usuario=Order.objects.filter(id=id).filter().first()
    orderitems = OrderItems.objects.filter(order=orden_usuario)
    context = {'orden_usuario':orden_usuario, 'orderitems':orderitems}
    return render(request, 'fiambres/pedido_historico_id.html', context)

def buscar_pedido2(request):
        ordenes_usuarios = Order.objects.filter().order_by('-id')
        context = {'ordenes_usuarios':ordenes_usuarios}
        return render(request, 'fiambres/listado_historico.html', context)



#Unidad de Medida


class ListarUnidadMedida(ValidarPermisosRequeridosMixin,ListView):
    model = UnidadMedida
    template_name = 'fiambres/listar_unidadmedida.html'
    permission_required = ('fiambres.view_unidadmedida','fiambres.add_unidadmedida','fiambres.delete_unidadmedida','fiambres.change_unidadmedida')
    context_object_name = 'unidadmedida'
    queryset = UnidadMedida.objects.all()
    paginate_by = 1


class EditarUnidadMedida(ValidarPermisosRequeridosMixin,UpdateView):
    model = UnidadMedida
    template_name = 'fiambres/modalunidadmedida.html'
    permission_required = ('fiambres.view_unidadmedida','fiambres.add_unidadmedida','fiambres.delete_unidadmedida','fiambres.change_unidadmedida')
    form_class = UnidadaMedidaForm
    success_url = reverse_lazy ('fiambres:listar_unidadmedida')


class CrearUnidadMedida(ValidarPermisosRequeridosMixin,CreateView):
    model = UnidadMedida
    form_class = UnidadaMedidaForm
    template_name = 'fiambres/crear_unidadmedida.html'
    permission_required = ('fiambres.view_unidadmedida','fiambres.add_unidadmedida','fiambres.delete_unidadmedida','fiambres.change_unidadmedida')
    success_url = reverse_lazy ('fiambres:listar_unidadmedida')

class CrearModalUnidadMedida(ValidarPermisosRequeridosMixin,CreateView):
    model = UnidadMedida
    template_name = 'fiambres/modalcrearunidadmedida.html'
    permission_required = ('fiambres.view_unidadmedida','fiambres.add_unidadmedida','fiambres.delete_unidadmedida','fiambres.change_unidadmedida')
    form_class = UnidadaMedidaForm
    success_url = reverse_lazy ('fiambres:listar_unidadmedida')
    

class EliminarUnidadMedida(ValidarPermisosRequeridosMixin,DeleteView):
    model = UnidadMedida
    permission_required = ('fiambres.view_unidadmedida','fiambres.add_unidadmedida','fiambres.delete_unidadmedida','fiambres.change_unidadmedida')
    success_url = reverse_lazy ('fiambres:listar_unidadmedida')

@permission_required('fiambres.view_unidadmedida',login_url='home')
@permission_required('fiambres.add_unidadmedida',login_url='home')
@permission_required('fiambres.delete_unidadmedida',login_url='home')
@permission_required('fiambres.change_unidadmedida',login_url='home')
def buscar_unidadmedida(request):
        busqueda = request.GET.get("buscar")
        unidadmedida = UnidadMedida.objects.all().order_by('-id')
        paginator = Paginator(unidadmedida, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if busqueda:
                unidadmedida = UnidadMedida.objects.filter(
                    Q (name__icontains = busqueda) |
                    Q (id__icontains= busqueda)
                ).distinct()
                return render(request, 'fiambres/listar_unidadmedida.html', {'unidadmedida':unidadmedida})
        else:
            return render(request, 'fiambres/listar_unidadmedida.html', {'unidadmedida': page_obj})


#Unidad de Medida


class ListarPrecios(ValidarPermisosRequeridosMixin,ListView):
    model = Precios
    template_name = 'fiambres/listar_precios.html'
    permission_required = ('fiambres.view_precios','fiambres.add_precios','fiambres.delete_precios','fiambres.change_precios')
    context_object_name = 'precios'
    queryset = Precios.objects.all()
    paginate_by = 1


class EditarPrecios(ValidarPermisosRequeridosMixin,UpdateView):
    model = Precios
    template_name = 'fiambres/modalprecios.html'
    permission_required = ('fiambres.view_precios','fiambres.add_precios','fiambres.delete_precios','fiambres.change_precios')
    form_class = PreciosForm
    success_url = reverse_lazy ('fiambres:listar_precios')


class CrearModalPrecios(ValidarPermisosRequeridosMixin,CreateView):
    model = Precios
    template_name = 'fiambres/modalcrearprecios.html'
    permission_required = ('fiambres.view_precios','fiambres.add_precios','fiambres.delete_precios','fiambres.change_precios')
    form_class = PreciosForm
    success_url = reverse_lazy ('fiambres:listar_precios')
    

class EliminarPrecios(ValidarPermisosRequeridosMixin,DeleteView):
    model = Precios
    permission_required = ('fiambres.view_precios','fiambres.add_precios','fiambres.delete_precios','fiambres.change_precios')
    success_url = reverse_lazy ('fiambres:listar_precios')

@permission_required('fiambres.view_precios',login_url='home')
@permission_required('fiambres.add_precios',login_url='home')
@permission_required('fiambres.delete_precios',login_url='home')
@permission_required('fiambres.change_precios',login_url='home')
def buscar_precios(request):
        busqueda = request.GET.get("buscar")
        precios = Precios.objects.all().order_by('-id')
        paginator = Paginator(precios, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if busqueda:
                precios = Precios.objects.filter(
                    Q (name__icontains = busqueda) |
                    Q (id__icontains= busqueda)
                ).distinct()
                return render(request, 'fiambres/listar_precios.html', {'precios':precios})
        else:
            return render(request, 'fiambres/listar_precios.html', {'precios': page_obj})

"""
def actualizar_precios():
    products = Product.objects.all()
    price_increase = Aumento.objects.all()
    for product in products:
        product.price = (float(product.price)*float(price_increase))
        product.save()
    return render ('fiambres/actualizar_precios.html',{'price_increase':price_increase})

"""




#Ofertas

def ofertas(request):
        busqueda = request.GET.get("buscar")
        cat=Categoria_Usuario.objects.all()
        #usuarios = Usuario.objects.filter(tipo_usuario = cat)
        #categoria_precio = Precios.objects.filter(tipo_usuario = request.tipo_usuario)
        products = Product.objects.filter(available=True, featured=True, categoria_usuario=request.user.tipo_usuario)
        categories = Category.objects.all()
        #paginator = Paginator(products, 20)
        #page_number = request.GET.get('page')
        #page_obj = paginator.get_page(page_number)

        if busqueda:
            products = Product.objects.filter(
                Q (name__icontains = busqueda) |
                Q (category__name__icontains = busqueda) |
                Q (price__icontains = busqueda)
            ).distinct()
            return render(request, 'fiambres/listado_productos.html', {'products':products, 'categories': categories, 'cat':cat})
        else:
            return render(request, 'fiambres/listado_productos.html', {'products': products, 'categories': categories, 'cat':cat})




