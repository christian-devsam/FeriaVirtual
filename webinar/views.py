from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.db import connection
from django.contrib.auth import authenticate, login, logout
import cx_Oracle
from django.views.generic import TemplateView
from .forms import UserCreationForm, CustomUserCreationForm
from django.contrib.auth.models import User, auth, Group
from django.contrib.auth.decorators import login_required, permission_required
from .models import Producto,Productor, Cliente, Transportista, Pedido, RegistroProducto, EstadoProducto, Producto, Subasta, DetallePedido
from django.shortcuts import redirect
from datetime import datetime
from django.db.models import Max
from django.shortcuts import get_object_or_404 

def home(request):
    # correo='god@gmail.com'
    # if User.objects.filter(email=correo).first() is not None:
    #     print('1')
    #     messages.info(request, 'El correo ya existe')
    #     return redirect(to='aboutus')
    # else:
    #     print('2')

    return render(request, 'webinartemp/InicioFeria.html')

def contacto(request):
    return render(request, 'webinartemp/Contacto.html')

def perfil(request):
    return render(request, 'webinartemp/perfil.html')

def aboutus(request):
    return render(request, 'webinartemp/aboutus.html')

def cambiocontrasena(request):
    return render(request, 'webinartemp/CambioContra.html')

@permission_required('webinar.add_pedido')
def compra(request):

    usc = User.objects.get(username=request.user.username)
    runnin = Cliente.objects.get(usuario=usc)
    identicliente = Pedido.objects.filter(rut_cli=runnin.rut_cli)
    idpedidoactuali = identicliente.aggregate(Max('id_pedido'))
    actualidpedido = idpedidoactuali['id_pedido__max']
    listardetalle= DetallePedido.objects.filter(id_pedido=actualidpedido).values()
    nomprod = Producto.objects.all().values()
    print(listardetalle)
    print(actualidpedido)
    print(nomprod)


    data={
       'listar_productos':listarproductos(),
       'listar_detalle':listardetalle,
       'listar_nombre':nomprod,
       'idpedi':actualidpedido,

    }

    if request.method == 'POST':

        usn = User.objects.get(username=request.user.username)
    
        run = Cliente.objects.get(usuario=usn) 

        id_producto = request.POST.get('proddisp')
        cantidad = request.POST.get('nrokg') 
        run = Cliente.objects.get(usuario=usn)
        identcliente = Pedido.objects.filter(rut_cli=run.rut_cli)
        idpedidoactual = identcliente.aggregate(Max('id_pedido'))
        actualidpedidos = idpedidoactual['id_pedido__max']

        salida = agregardetalle(idpedidoactual['id_pedido__max'],id_producto,cantidad)

        listardetalle= DetallePedido.objects.filter(id_pedido=actualidpedidos)

        if salida == 1:
            data ['mensaje']= 'Agregado Correctamente'

        else:
            data ['mensaje'] = 'No se pudo agregar'

    
    return render(request, 'webinartemp/Compra.html', data)

def confirmacionpedido(request):
    return render(request, 'webinartemp/ConfirmacionPedido.html')

def creacionusuario(request):
    data={
       'listar_regiones':listarregiones(),
       'listar_provincias':listarprovincia(),
       'listar_comunas':listarcomunas(),
    }

    if request.method == 'POST':

        rut_cli = request.POST.get('ruti')
        id_tipocliente = 1
        nombre = request.POST.get('nombree')
        apellido = request.POST.get('apellidop')
        direccion = request.POST.get('direcciom')
        telefono = request.POST.get('telefonos')
        correo = request.POST.get('correos')
        region = request.POST.get('regions')
        provincia = request.POST.get('provincias')
        comuna = request.POST.get('comunass')
        usuario = request.POST.get('usernams')
        contrasenia = request.POST.get('contra')
        id_pais = 1 

        if User.objects.filter(email=correo).first() is not None:
            print('1')
            messages.info(request, 'El correo ya existe')
            return redirect(to='/registrar/')
        elif User.objects.filter(username=usuario).first() is not None:
            messages.info(request, 'El nombre de Usuario ya existe')
            return redirect(to='/registrar/')
        else:

            salida=agregarcliente(rut_cli, id_tipocliente, nombre, apellido,  direccion, telefono, correo, region, provincia, comuna, usuario, contrasenia, id_pais)

            if salida == 1:
                data ['mensaje']= 'Agregado Correctamente'

            try:
                u = User.objects.get(email=correo)
                messages.info(request, 'El correo ya existe')
                return redirect(registrar)
            except:
                    
                group = Group.objects.get(name='c_local')
                u = User()
                u.first_name = nombre
                u.last_name  = apellido
                u.username   = usuario
                u.email      = correo
                u.set_password(contrasenia)
                u.save()
                group = Group.objects.get(name='c_local')
                u.groups.add(group)

            else:
                data ['mensaje'] = 'No se pudo agregar'

    return render(request, 'webinartemp/CreacionUsuario.html', data)

def sesionmain (request):
    if request.method=="POST":
        usuario = request.POST['user']
        contrasenia = request.POST['cont']

        Cliente = auth.authenticate(username=usern,password=cont)

        group = Group.objects.get(name='c_local')
        group2 = Group.objects.get(name='c_productor')
        group3 = Group.objects.get(name='c_transportista')

        if Cliente is not None:
            
            auth.login(request, cliente)
            return redirect("iniciointerno")
        else:
            message.info(request,'invalido')
            return redirect("login")

    else:
        return render(request, 'registration/registro.html')




@permission_required('webinar.add_pedido')
def iniciointerno(request):
    return render(request, 'webinartemp/InicioInterno.html')

@permission_required('webinar.add_producto')
def inicioproveedor(request):
    return render(request, 'webinartemp/InicioProveedor.html')

@permission_required('webinar.add_puja')
def iniciotransportista(request):
    return render(request, 'webinartemp/InicioTransportista.html')

@permission_required('webinar.change_pedido')
def listadopedidoscliente(request):
    usn = User.objects.get(username=request.user.username)
    
    if Cliente.objects.filter(usuario=usn):
        
        
        run = Cliente.objects.get(usuario=usn)
        pedido = Pedido.objects.filter(rut_cli=run).values()
        prod =  Producto.objects.all().values()
        detped = DetallePedido.objects.all().values()
        data = {
        'pedidos': pedido,
        'products': prod,
        'detalle':detped,
        }

        print(pedido)

    else:
        
        return render(request, 'webinartemp/ListadoPedidosCliente.html')
        
    print (pedido)
    return render(request, 'webinartemp/ListadoPedidosCliente.html',data)

@permission_required('webinar.view_subasta')
def listadosubastasganadas(request):
    return render(request, 'webinartemp/ListadoSubastasGanadas.html')

@permission_required('webinar.view_subasta')
def listadosubastasing(request):
    return render(request, 'webinartemp/ListadoSubastasIng.html')

@permission_required('webinar.add_producto')
def paginacontratos(request):
    return render(request, 'webinartemp/PaginaContratos.html')

@permission_required('webinar.view_pedido')
def paginapedidos(request):
    if request.method=="POST":
        usn = User.objects.get(username=request.user.username)
        run = Cliente.objects.get(usuario=usn) 
        crearpedido(run.rut_cli)
        return redirect(compra)
        
    return render(request, 'webinartemp/PaginaPedidos.html')

@permission_required('webinar.view_producto')
def paginaproductos(request):
    data={
       'listar_productos':listarproductos(),
       'listar_estado':listarestado(),
       'listar_cat_feria':listarcategoriaferia(),
    }

    if request.method == 'POST':

        usn = User.objects.get(username=request.user.username)
        run = Productor.objects.get(usuario=usn)

        rut_pro = run.rut_pro
        id_producto = request.POST.get('proddisp')
        id_estado = request.POST.get('estadoprod')
        id_categoria = request.POST.get('catferia')
        id_bodega = 1
        fecha_ingreso = datetime.now().date()
        cantidad_kg = request.POST.get('kiloscan')
        precio_kg = request.POST.get('preciokil')      
        
        salida=agregarproducto(rut_pro, id_producto, id_estado, id_categoria,  id_bodega, fecha_ingreso, cantidad_kg, precio_kg)

        if salida == 1:
            data ['mensaje']= 'Agregado Correctamente'

        else:
            data ['mensaje'] = 'No se pudo agregar'

    return render(request, 'webinartemp/PaginaProductos.html',data)

@permission_required('webinar.view_producto')
def listadoproductosproductor(request):

    usn = User.objects.get(username=request.user.username)
    if Productor.objects.filter(usuario=usn):

        run = Productor.objects.get(usuario=usn)
        rutpros= RegistroProducto.objects.filter(rut_pro=run).values()
        rutprod = RegistroProducto.objects.filter(rut_pro=run)
        prodnom = Producto.objects.all().values()
        est = EstadoProducto.objects.all().values()

        data = {
            'regprod': rutpros,
            'nomprodu':prodnom,
            'estadopr':est,
            
            
        }

    else:
        
        return render(request, 'webinartemp/listadoproductos.html')



    # rutpro= run.rut_pro
    # productos_produc = listarproductosporrut(rutpro)


    # data={
    #     'productos_prod':productos_produc
    # }

    # print(data)

    return render(request, 'webinartemp/listadoproductos.html',data)

@permission_required('webinar.view_subasta')
def paginapujar(request):
    
    if request.method=="POST":

        data = {
            'list_idsub':listaridsub(),
        }

        

    return render(request, 'webinartemp/PaginaPujar.html', data)

@permission_required('webinar.view_subasta')
def paginasubastas(request):

    subs = Subasta.objects.filter(id_estado=1).values()
    data={
        'listarsub':subs
    }
    return render(request, 'webinartemp/PaginaSubastas.html', data)

def postulacion(request):
    return render(request, 'webinartemp/Postulacion.html')

@permission_required('webinar.view_subasta')
def seguimiento(request):
    return render(request, 'webinartemp/Seguimiento.html')

@permission_required('webinar.view_subasta')
def subastaadentro(request):

    data={

    }

    if request.method =="POST":

        usn = User.objects.get(username=request.user.username)
        run = Transportista.objects.get(usuario=usn)

        id_subasta = 1
        id_transportista = run.id_transportista
        valor = request.POST.get("pujat")

        salida=agregarpuja(id_subasta, id_transportista, valor)

        if salida == 1:
            data ['mensaje']= 'Agregado Correctamente'

        else:
            data ['mensaje'] = 'No se pudo agregar'


    
    return render(request, 'webinartemp/SubastaAdentro.html',data)


@permission_required('webinar.view_subasta')
def transportecont(request):
    return render(request, 'webinartemp/TransporteContrato.html')

def listadoadmin():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_ADMIN", [out_cur])

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def obtenerusuario():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_OBTENERUSUARIO", [out_cur])

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

##<-------------------------------------FUNCIONES LUGARES---------------------------------------------------->

def listarregiones():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_regiones", [out_cur])

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def listarcomunasporid(regionid):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_region_por_categoria", [out_cur, regionid])

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def listarprovinciasporregion(regionid):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_region_por_categoria", [out_cur, regionid])

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def listarcomunasporprovincia(provinciaid):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PROVINCIA_POR_CATEGORIA", [out_cur, provinciaid])

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def listarcomunasporprovincia(provinciaid):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PROVINCIA_POR_CATEGORIA", [out_cur, provinciaid])

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def listarprovincia():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_provincias", [out_cur])

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def provinciaporregion(request):
    region = request.GET.get('region')
    data = {
        'provregion':listarprovinciasporregion(region)
    }

    return render(request, 'webinartemp/combobox_provregion.html', data)

def comunaporprovincia(request):
    provincia = request.GET.get('provincia')
    data = {
        'provcomuna':listarcomunasporprovincia(provincia)
    }

    return render(request, 'webinartemp/combobox_provcomuna.html', data)

def listarcomunas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_comunas", [out_cur])

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

##<----------------------------------------- FUNCIONES PRODUCTOS ------------------------------------->

def listarproductos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_productos", [out_cur])

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def listarproductosdisponibles():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_productos_dispo", [out_cur])

    productos = Producto.objects.all()

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def listarestado():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_estado", [out_cur])

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def listarcategoriaferia():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_cat_feria", [out_cur]) 

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def listarproductosporrut(rutpro):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_productos_productor", [out_cur, rutpro])

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def eliminar_detalle_pedido(request, id_pedido_id,id_producto_id):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()

    cursor.callproc("sp_eliminar_detalle", [id_pedido_id, id_producto_id])

    return redirect(to="compra")

def eliminar_pedido(request,id_pedido_id):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()

    cursor.callproc("sp_eliminar_pedido", [id_pedido_id])

    return redirect(to="paginapedidos")

def detalle_pedido_ver(id_pedido):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_detalles", [out_cur, id_pedido])

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def detallepedido(request):
    idped = request.GET.get('idped')
    data = {
        'pedidos':detalle_pedido_ver(idped)
    }

    return render(request, 'webinartemp/detalle.html',data)

##<----------------------------------------FUNCIONES PEDIDOS------------------------------------------------------>

def listar_pedidos(request):
    usn = User.objects.get(username=request.user.username)
    run = Cliente.objects.get(usuario=usn)
    pedido = Pedido.objects.filter(rut_cli=run).values()
    print (pedido)

# def agregarclientene():
    
#     usern = Cliente.objects.all()
    
#     field_name = 'contrasenia'
#     obj = Cliente.objects.first()
#     field_object = Cliente._meta.get_field(field_name)
#     field_value = field_object.value_from_object(obj)

#     try:
#         u = User.objects.get(email=correo)
#         messages.info(request, 'El correo ya existe')
#         return redirect(registrar)
#     except:
                
#         group = Group.objects.get(name='c_local')
#         u = User()
#         u.first_name = nombre
#         u.last_name  = apellido
#         u.username   = usuario
#         u.email      = correo
#         u.set_password(contrasenia)
#         u.save()
#         group = Group.objects.get(name='c_local')
#         u.groups.add(group)

#     print (usern)
#     print (field_value)

# def agregarclientene():
    
#     # usern = Cliente.objects.all()
    
#     # for x in usern


def listaridpedido(rut_cli):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_idpedido", [out_cur, rut_cli]) 

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def listarsubasta():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_subasta", [out_cur]) 

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def listaridsub():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_idsub", [out_cur]) 

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def listarnombreprod():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_idsub", [out_cur]) 

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista

def obteneridpedido():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_obtener_idpedido", [out_cur]) 

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista


def listares():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_idsub", [out_cur]) 

    lista=[]
    for fila in out_cur:
        lista.append(fila)

    return lista


##<---------------------------AGREGAR COSAS---------------------------------------------------------------------------->
def agregarcliente(rut_cli, id_tipocliente, nombre, apellido, direccion, telefono, correo, region, provincia, comuna, usuario, contrasenia, id_pais):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_CLIENTE', [rut_cli, id_tipocliente, nombre, apellido,  direccion, telefono, correo, region, provincia,comuna, usuario, contrasenia,id_pais, salida])
    return salida.getvalue()

def agregarproducto(rut_pro, id_producto, id_estado, id_categoria,  id_bodega, fecha_ingreso, cantidad_kg, precio_kg):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_PRODUCTO', [rut_pro, id_producto, id_estado, id_categoria,  id_bodega, fecha_ingreso, cantidad_kg, precio_kg, salida])
    return salida.getvalue()

def agregardetalle(id_pedido, id_producto, cantidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_DETALLE', [id_pedido,id_producto, cantidad, salida])
    return salida.getvalue()

def agregarpuja(id_subasta, id_transportista, valor):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_PUJA', [id_subasta, id_transportista, valor, salida])
    return salida.getvalue()

def crearpedido(rut_cli):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_PEDIDO', [rut_cli])

def handle_not_found(request, exception):
    return render(request, 'webinartemp/404_page.html')

def listardetallespedidos(id_pedido):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.TextField)
    cursor.callproc("sp_idk2", [salida, id_pedido]) 

    return salida.TextField()