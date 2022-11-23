from django.urls import path,re_path
from django.contrib.auth.decorators import login_required
from .views import CrearCategorias, CrearModalPrecios, CrearModalProductos, CrearModalUnidadMedida, CrearProductos, CrearUnidadMedida, EditarPrecios, EditarProductos, EditarUnidadMedida, EliminarPrecios, EliminarProductos, EliminarUnidadMedida, buscar_categoriass, buscar_pedido2, buscar_precios, buscar_productos, buscar_unidadmedida, buscar_usuarios_ordenes_historico, checkout, listado_productos,buscar_categorias,detail, ListadoPedidos, ofertas, pagar
from .views import CrearCategorias, CrearModalCategorias, EditarCategorias, EliminarCategorias, buscar_usuarios_ordenes, buscar_usuarios_ordenes_id,VerPedido, buscar_pedido, buscar_pedido_id

app_name='fiambres'


urlpatterns = [
    path('listado_productos/', login_required(listado_productos), name = 'listado_productos'),
    path('home/', login_required(listado_productos), name = 'home'),
    path('listado_pedidos/', login_required(ListadoPedidos.as_view()), name='listado_pedidos'),
    path('categories/<id>', login_required(buscar_categoriass), name = 'categories'),
    path('detail/<slug>', login_required(detail), name = 'detail'),
    path('checkout/', login_required(checkout), name = 'checkout'),
    #path('<slug>/cart', login_required(Cart()), name = 'Cart'),

    
    path('crear_productos/', login_required(CrearProductos.as_view()), name = 'crear_productos'),
    path('crear__productos/', login_required(CrearModalProductos.as_view()), name = 'crear__productos'),
    path('listar_productos/', login_required(buscar_productos), name = 'listar_productos'),
    path('editar_productos/<int:slug>', login_required(EditarProductos.as_view()), name = 'editar_productos'),
    path('eliminar_productos/<int:slug>',login_required(EliminarProductos.as_view()), name = 'eliminar_productos'),

    path('crear_categorias/', login_required(CrearCategorias.as_view()), name = 'crear_categorias'),
    path('crear__categorias/', login_required(CrearModalCategorias.as_view()), name = 'crear__categorias'),
    path('listar_categorias/', login_required(buscar_categorias), name = 'listar_categorias'),
    path('editar_categorias/<int:pk>', login_required(EditarCategorias.as_view()), name = 'editar_categorias'),
    path('eliminar_categorias/<int:pk>',login_required(EliminarCategorias.as_view()), name = 'eliminar_categorias'),

    path('crear_unidadmedida/', login_required(CrearUnidadMedida.as_view()), name = 'crear_unidadmedida'),
    path('crear__unidadmedida/', login_required(CrearModalUnidadMedida.as_view()), name = 'crear__unidadmedida'),
    path('listar_unidadmedida/', login_required(buscar_unidadmedida), name = 'listar_unidadmedida'),
    path('editar_unidadmedida/<int:pk>', login_required(EditarUnidadMedida.as_view()), name = 'editar_unidadmedida'),
    path('eliminar_unidadmedida/<int:pk>',login_required(EliminarUnidadMedida.as_view()), name = 'eliminar_unidadmedida'),

    path('crear__precios/', login_required(CrearModalPrecios.as_view()), name = 'crear__precios'),
    path('listar_precios/', login_required(buscar_precios), name = 'listar_precios'),
    path('editar_precios/<int:pk>', login_required(EditarPrecios.as_view()), name = 'editar_precios'),
    path('eliminar_precios/<int:pk>',login_required(EliminarPrecios.as_view()), name = 'eliminar_precios'),
    #path('actualizar_precios/', login_required(actualizar_precios()), name = 'actualizar_precios'),

    path('listar_ordenes_usuario/', login_required(buscar_usuarios_ordenes), name = 'listar_ordenes_usuario'),
    path('listar_ordenes_historico/', login_required(buscar_usuarios_ordenes_historico), name = 'listar_ordenes_historico'),
    path('listar_ordenes_usuario_id/<id>', login_required(buscar_usuarios_ordenes_id), name = 'listar_ordenes_usuario_id'),
    path('pago2/', login_required(pagar), name = 'pago2'),


    path('pedido_historico/', login_required(buscar_pedido), name = 'pedido_historico'),
    path('pedido_historico_id/<id>', login_required(buscar_pedido_id), name = 'pedido_historico_id'),
    path('editar_orden/<int:pk>', login_required(VerPedido.as_view()), name = 'editar_orden'),
    path('listado_historico/', login_required(buscar_pedido2), name = 'listado_historico'),

    path('ofertas/', login_required(ofertas), name = 'ofertas'),

    ]

