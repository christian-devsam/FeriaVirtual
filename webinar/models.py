# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User, auth, Group


class Administrador(models.Model):
    id_adm = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.BigIntegerField()
    correo = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    usuario = models.CharField(max_length=20)
    contrasenia = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'administrador'

    def __str__(self):
        return self.usuario


class Bodega(models.Model):
    id_bodega = models.BigIntegerField(primary_key=True)
    comuna = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'bodega'
    
    def __str__(self):
        return self.direccion


class Categoria(models.Model):
    id_categoria = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'categoria'

    def __str__(self):
        return self.descripcion


class Cliente(models.Model):

    rut_cli = models.CharField(primary_key=True, max_length=20)
    id_tipocliente = models.ForeignKey('TipoCliente', models.DO_NOTHING, db_column='id_tipocliente')
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.BigIntegerField()
    correo = models.CharField(max_length=50)
    usuario = models.CharField(max_length=20)
    contrasenia = models.CharField(max_length=20)
    id_cliente = models.BigIntegerField()
    id_pais = models.ForeignKey('Pais', models.DO_NOTHING, db_column='id_pais')
    region = models.ForeignKey('Region', models.DO_NOTHING)
    provincia = models.ForeignKey('Provincia', models.DO_NOTHING)
    id_comuna = models.ForeignKey('Comuna', models.DO_NOTHING, db_column='id_comuna')

    class Meta:
        managed = False
        db_table = 'cliente'
    
    def __str__(self):
        return self.usuario


            

    


class Comuna(models.Model):
    id_comuna = models.BigIntegerField(primary_key=True)
    comuna = models.CharField(max_length=64)
    provincia = models.ForeignKey('Provincia', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comuna'
    
    def __str__(self):
        return self.comuna


class Consultor(models.Model):
    id_consultor = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    telefono = models.BigIntegerField()
    direccion = models.CharField(max_length=50)
    usuario = models.CharField(max_length=20)
    contrasenia = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'consultor'

    def __str__(self):
        return self.usuario


class Contrato(models.Model):
    id_contrato = models.BigIntegerField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    vigencia = models.CharField(max_length=1)
    rut_pro = models.ForeignKey('Productor', models.DO_NOTHING, db_column='rut_pro')
    rut_cli = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='rut_cli')
    observaciones = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'contrato'
        unique_together = (('id_contrato', 'rut_pro', 'rut_cli'),)
    
    def __str__(self):
        return self.id_contrato


class ContratoTransporte(models.Model):
    id_contrato = models.BigIntegerField(primary_key=True)
    vigencia = models.CharField(max_length=1)
    id_transportista = models.ForeignKey('Transportista', models.DO_NOTHING, db_column='id_transportista')
    id_seguro = models.ForeignKey('Seguro', models.DO_NOTHING, db_column='id_seguro')

    class Meta:
        managed = False
        db_table = 'contrato_transporte'
    
    def __str__(self):
        return self.id_contrato


class DetallePedido(models.Model):
    id_pedido = models.OneToOneField('Pedido', models.DO_NOTHING, db_column='id_pedido', primary_key=True)
    id_producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='id_producto')
    cantidad = models.BigIntegerField()
    valor = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalle_pedido'
        unique_together = (('id_pedido', 'id_producto'),)
        


class EstadoProducto(models.Model):
    id_estado = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'estado_producto'
    
    def __str__(self):
        return self.descripcion


class EstadoSubasta(models.Model):
    id_estado = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'estado_subasta'

    def __str__(self):
        return self.descripcion


class LicenciaConducir(models.Model):
    id_licencia = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'licencia_conducir'
    
    def __str__(self):
        return self.nombre


class OrdenCompra(models.Model):
    id_orden = models.BigIntegerField(primary_key=True)
    detalles = models.CharField(max_length=50)
    cantidad = models.BigIntegerField()
    id_adm = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='id_adm')
    rut_pro = models.ForeignKey('Productor', models.DO_NOTHING, db_column='rut_pro')

    class Meta:
        managed = False
        db_table = 'orden_compra'
        unique_together = (('id_orden', 'id_adm', 'rut_pro'),)
    
    def __str__(self):
        return self.id_orden


class Pago(models.Model):
    id_pago = models.BigIntegerField(primary_key=True)
    estado = models.CharField(max_length=50)
    id_pedido = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'pago'
    
    def __str__(self):
        return self.estado


class Pais(models.Model):
    id_pais = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'pais'

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    id_pedido = models.BigIntegerField(primary_key=True)
    fecha_ingreso = models.DateField()
    fecha_envio = models.DateField()
    rut_cli = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='rut_cli')
    sub_total = models.BigIntegerField(blank=True, null=True)
    p_transporte = models.BigIntegerField(blank=True, null=True)
    comision_mg = models.BigIntegerField(blank=True, null=True)
    total_pagar = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedido'

    def __str__(self):
        return self.id_pedido


class Producto(models.Model):
    id_producto = models.BigIntegerField(primary_key=True)
    nombre_producto = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'producto'
    
    def __str__(self):
        return self.nombre_producto


class Productor(models.Model):
    rut_pro = models.CharField(primary_key=True, max_length=20)
    nombres = models.CharField(max_length=50)
    apellido_pat = models.CharField(max_length=50)
    apellido_mat = models.CharField(max_length=50)
    direccion = models.CharField(max_length=70)
    telefono = models.BigIntegerField()
    correo = models.CharField(max_length=200)
    fecha_creacion = models.DateField()
    usuario = models.CharField(max_length=20)
    contrasenia = models.CharField(max_length=20)
    id_productor = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'productor'
    
    def __str__(self):
        return self.usuario


class Provincia(models.Model):
    provincia_id = models.BigIntegerField(primary_key=True)
    provincia = models.CharField(max_length=64)
    region = models.ForeignKey('Region', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'provincia'
    
    def __str__(self):
        return self.provincia


class Puja(models.Model):
    id_subasta = models.OneToOneField('Subasta', models.DO_NOTHING, db_column='id_subasta', primary_key=True)
    id_transportista = models.ForeignKey('Transportista', models.DO_NOTHING, db_column='id_transportista')
    valor = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'puja'
        unique_together = (('id_subasta', 'id_transportista'),)
    
    def __str__(self):
        return self.valor


class Region(models.Model):
    region_id = models.BigIntegerField(primary_key=True)
    region = models.CharField(max_length=64)
    abreviatura = models.CharField(max_length=64)
    capital = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'region'

    def __str__(self):
        return self.region


class RegistroProducto(models.Model):
    rut_pro = models.OneToOneField(Productor, models.DO_NOTHING, db_column='rut_pro', primary_key=True)
    id_producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='id_producto')
    id_estado = models.ForeignKey(EstadoProducto, models.DO_NOTHING, db_column='id_estado')
    id_categoria = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='id_categoria')
    id_bodega = models.ForeignKey(Bodega, models.DO_NOTHING, db_column='id_bodega')
    fecha_ingreso = models.DateField(blank=True, null=True)
    cantidad_kg = models.BigIntegerField(blank=True, null=True)
    precio_kg = models.BigIntegerField(blank=True, null=True)
    cantidad_unidad = models.BigIntegerField(blank=True, null=True)
    precio_unidad = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registro_producto'
        unique_together = (('rut_pro', 'id_producto'),)



class Reporte(models.Model):
    id_reporte = models.BigIntegerField()
    descripcion = models.CharField(max_length=80)
    estado = models.CharField(max_length=50)
    id_consultor = models.OneToOneField(Consultor, models.DO_NOTHING, db_column='id_consultor', primary_key=True)
    id_adm = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='id_adm')

    class Meta:
        managed = False
        db_table = 'reporte'
        unique_together = (('id_consultor', 'id_reporte', 'id_adm'),)
    
    def __str__(self):
        return self.estado


class Seguro(models.Model):
    id_seguro = models.BigIntegerField(primary_key=True)
    empresa = models.CharField(max_length=50)
    detalles = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'seguro'
    
    def __str__(self):
        return self.empresa


class Subasta(models.Model):
    id_subasta = models.BigIntegerField(primary_key=True)
    fecha_ingreso = models.DateField()
    fecha_termino = models.DateField()
    id_pedido = models.ForeignKey(Pedido, models.DO_NOTHING, db_column='id_pedido')
    id_estado = models.ForeignKey(EstadoSubasta, models.DO_NOTHING, db_column='id_estado')

    class Meta:
        managed = False
        db_table = 'subasta'
    

        


class TipoCliente(models.Model):
    id_tipocliente = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'tipo_cliente'
    
    def __str__(self):
        return self.descripcion


class Transporte(models.Model):
    id_transporte = models.BigIntegerField(primary_key=True)
    categoria = models.CharField(max_length=50)
    tamano = models.CharField(max_length=50)
    refrigeracion = models.CharField(max_length=50)
    capacidad_carga = models.CharField(max_length=50)
    id_transportista = models.ForeignKey('Transportista', models.DO_NOTHING, db_column='id_transportista')
    patente = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'transporte'
        unique_together = (('id_transporte', 'id_transportista'),)
    
    def __str__(self):
        return self.patente


class Transportista(models.Model):
    id_transportista = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.BigIntegerField()
    usuario = models.CharField(max_length=20)
    contrasenia = models.CharField(max_length=20)
    correo = models.CharField(max_length=80)
    id_licencia = models.ForeignKey(LicenciaConducir, models.DO_NOTHING, db_column='id_licencia')

    class Meta:
        managed = False
        db_table = 'transportista'
    
    def __str__(self):
        return self.usuario


class Usuario(models.Model):
    id = models.BigIntegerField(primary_key=True)
    usuario = models.CharField(max_length=20)
    contrasenia = models.CharField(max_length=20, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'usuario'
    
    def __str__(self):
        return self.usuario
