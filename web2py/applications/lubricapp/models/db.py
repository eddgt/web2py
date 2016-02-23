# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    #db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
    db=DAL('mysql://root:@localhost/lubricappdb')

else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)


#CODE BY OSMANGT 21-04-2015
ARTICULOS= [("Filtro de Aire","Caterpillar",100, 10.34, "unds"), ("Filtro de Aceite","Caterpillar", 200,32.32, "unds"),
            ("Grasa molly","Caterpillar",300, 2.32, "Kg"), ("Filtro Hidraulico","Caterpillar", 400,32.33, "unds"),
            ("Aceite 15W40","shell",500, 19.34, "Kg"), ("Tapa de Radiador","shell",150, 23.21, "unds"),
            ("Aceite Hid 10W30","shell",100, 24.12, "Kg"), ("Desengrasante","shell",200, 12.34, "Kg"),
            ("Aceite Trans","mobil",420, 10.03, "Kg"), ("Wipe","n/a",650, 20.30, "Kg")
            ]

EQUIPO= [
		("MT00001","Tractor","CAT", "D9N", "Maquinaria","T000000001","2000","TR00002","CAT","3408","SM00005022","200","5000",2.50,10.00),
		("MT00002","Tractor","CAT", "D8N", "Maquinaria","T000000010","2002","TR00005","CAT","3406","SM00105002","150","4000",2.00,8.00),
		("VL00001","Pick Up","Mitsubishi", "2003", "Vehiculo Liviano","VLSC0001","2003","TRV00001","Mitsubishi","M0001","SM00105002","150","3000",2.00,8.00)
]

EMPLEADOS = [("Michael", "Guatemala City","456"), ("John", "Villa Nueva, Guatemala","123"),
             ("Graham", "Jutiapa, Guatemala","789"), ("Terry", "San Juan Sacatepequez","102"),
             ("Eric", "Guatemala City","567")]

ESTADOS = {"abierta": T("Abierta"), "bloqueada": T("Bloqueada"),
            "cancelada": T("Cancelada")}

UNIDADES = ["unds", "Kg", "g", "l"]

db.define_table("articulo",
                Field("descripcion"),
                Field("marca"),
                Field("saldo", "double", default=0.00),
                Field("precio", "double", default=0.00),
                Field("medida", requires=IS_IN_SET(UNIDADES),
                      default="unds"),
                format="%(descripcion)s: (%(medida)s)")


db.define_table("empleado",
                Field("nombre"),
                Field("direccion"),
                Field("nit"),
                format="%(nombre)s (%(nit)s)")


db.define_table("movimiento",
                Field("creada_en", "datetime", default=request.now),
                Field("creada_por", "reference auth_user",
                      default=auth.user_id, writable=False),
                Field("empleado_id", "reference empleado"),
                Field("descripcion"),
                Field("total", "double",
                      writable=False, default=0.00),
                Field("status", requires=IS_IN_SET(ESTADOS),
                      default="abierto", writable=False),
                format="%(id)s")

db.define_table("detalle_movimiento",
                Field("movimiento_id", "reference movimiento",
                      default=session.movimiento_id,
                      writable=False),
                Field("articulo_id", "reference articulo"),
                Field("cantidad", "double", default=0.00),
                Field("total", "double", default=0.00,
                      writable=False),
                format=lambda record: record.articulo_id.descripcion)


db.define_table("grupos",
                Field("descripcion"),
                Field("uso"),
                format="%(descripcion)s")

db.define_table("equipo",
                Field("codigo"),
                Field("descripcion"),
                Field("marca"),
                Field("modelo"),
                Field("grupo_id", "reference grupos"),
                Field("serie"),
                Field("anio"),
                Field("transmision"),
                Field("marca_motor"),
                Field("modelo_motor"),
                Field("serie_motor"),
                Field("hp_motor"),
                Field("cc_motor"),
                Field("peso", "double", default=0.00),
                Field("capacidad_tons", "double", default=0.00),
                format=lambda record: record.grupo_id.descripcion)


# Here we link moviento ids to the movimiento_detalle page.
db.movimiento.id.represent = lambda id, field: \
    A(id, _href=URL(c="default", f="movimiento", args=["movimiento", id]))

# Automatically add dummy data (not recommended in production)
if db(db.empleado).count() <= 0:
    for empleado in EMPLEADOS:
        db.empleado.insert(nombre=empleado[0],
                           direccion=empleado[1],
                           nit=empleado[2])
    for articulo in ARTICULOS:
       db.articulo.insert(descripcion=articulo[0], marca=articulo[1],saldo=articulo[2],
                         precio=articulo[3],medida=articulo[4])

if db(db.equipo).count() <= 0:
    for equipo in EQUIPO:
        db.equipo.insert(codigo=equipo[0],descripcion=equipo[1],marca=equipo[2],modelo=equipo[3],
                         grupo=equipo[4],serie=equipo[5],anio=equipo[6],transmision=equipo[7],
                         marca_motor=equipo[8],modelo_motor=equipo[9],serie_motor=equipo[10],
                         hp_motor=equipo[11],cc_motor=equipo[12],peso=equipo[13],capacidad_tons=equipo[14])

def movimiento_total(movimiento):
    if movimiento.status in ("bloqueada", "cancelada"): return
    items = db(db.detalle_movimiento.movimiento_id==movimiento.id).select()
    total = 0.00
    for item in items:
        item_total = item.cantidad * item.articulo_id.precio
        item.update_record(total=item_total)
        total += item_total
    movimiento.update_record(total=total)
