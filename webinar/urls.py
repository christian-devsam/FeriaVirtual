from django.urls import path
from . import views
from .views import creacionusuario, sesionmain, provinciaporregion, comunaporprovincia, eliminar_detalle_pedido, eliminar_pedido, detallepedido

urlpatterns = [
    path('', views.home, name="home"),
    path('contacto', views.contacto, name="contacto"),
    path('aboutus', views.aboutus, name="aboutus"),
    path('sesionmain', sesionmain, name="sesionmain"),
    path('cambiocontra', views.cambiocontrasena, name="cambiocontrasena"),
    path('compra', views.compra, name="compra"),
    path('confirmacionpedido', views.confirmacionpedido, name="confirmacionpedido"),
    path('creacionusuario', views.creacionusuario, name="creacionusuario"),
    path('iniciointerno', views.iniciointerno, name="iniciointerno"),
    path('inicioproveedor', views.inicioproveedor, name="inicioproveedor"),
    path('iniciotransportista', views.iniciotransportista, name="iniciotransportista"),
    path('listadopedidoscliente', views.listadopedidoscliente, name="listadopedidoscliente"),
    path('listadosubastasganadas', views.listadosubastasganadas, name="listadosubastasganadas"),
    path('listadosubastasing', views.listadosubastasing, name="listadosubastasing"),
    path('paginacontratos', views.paginacontratos, name="paginacontratos"),
    path('paginapedidos', views.paginapedidos, name="paginapedidos"),
    path('paginaproductos', views.paginaproductos, name="paginaproductos"),
    path('paginapujar', views.paginapujar, name="paginapujar"),
    path('paginasubastas', views.paginasubastas, name="paginasubastas"),
    path('postulacion', views.postulacion, name="postulacion"),
    path('seguimiento', views.seguimiento, name="seguimiento"),
    path('subastaadentro', views.subastaadentro, name="subastaadentro"),
    path('transportecontrato', views.transportecont, name="transportecontrato"),
    path('perfil', views.perfil, name="perfil"),
    path('provregiones/', provinciaporregion, name="provincia_por_region"),
    path('provcomunas/', comunaporprovincia, name="provincia_por_region"),
    path('listadoproductosproductor', views.listadoproductosproductor, name="listadoproductosproductor"),
    path('eliminardetallepedido/<id_pedido_id>/<id_producto_id>/', eliminar_detalle_pedido, name="eliminardetallepedido"),
    path('eliminarpedido/<id_pedido_id>/', eliminar_pedido, name="eliminarpedido"),
    path('detallepedido/', detallepedido, name="detallepedidover"),

]