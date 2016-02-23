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
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
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

##agrepado para tutorial blog 19052014:15hrs
from gluon.tools import Auth
auth=Auth(globals(),db)
auth.define_tables()

##agrepado para tutorial blog 19052014:15hrs
from gluon.tools import Crud
crud=Crud(globals(),db)

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
#mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'oulloa@televida.biz'
mail.settings.login = 'oulloa@televida.biz:televida.'

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
db.define_table('articulo',
   Field('titulo',length=256),
   Field('texto','text',requires=IS_NOT_EMPTY()),
   Field('autor',db.auth_user),
   Field ('imagen','upload'))

db.define_table('comentario',
   Field('articulo',db.articulo,writable=False,readable=False),
   Field('autor',db.auth_user,writable=False,readable=False),
   Field('texto','text',requires=IS_NOT_EMPTY()))

ITEMS= [("Filtro de Aire","Caterpillar",100, 10.34, "unds"), ("Filtro de Aceite","Caterpillar", 200,32.32, "unds"),
            ("Grasa molly","Caterpillar",300, 2.32, "Kg"), ("Filtro Hidraulico","Caterpillar", 400,32.33, "unds"),
            ("Aceite 15W40","shell",500, 19.34, "Kg"), ("Tapa de Radiador","shell",150, 23.21, "unds"),
            ("Aceite Hid 10W30","shell",100, 24.12, "Kg"), ("Desengrasante","shell",200, 12.34, "Kg"),
            ("Aceite Trans","mobil",420, 10.03, "Kg"), ("Wipe","n/a",650, 20.30, "Kg")
            ]

UNIDADES = ["unds", "Kg", "g", "l"]

db.define_table("items",
                Field("descripcion"),
                Field("marca"),
                Field("saldo", "double", default=0.00),
                Field("precio", "double", default=0.00),
                Field("medida", requires=IS_IN_SET(UNIDADES),
                      default="unds"),
                format="%(descripcion)s: (%(medida)s)")


db.define_table('factura',
   Field('numero'),
   Field('fecha',length=256),
   Field('cliente',requires=IS_NOT_EMPTY()),
   Field('autor',db.auth_user))

db.define_table('item_factura',
   Field('factura_id','reference factura',default=session.factura_id,
                      writable=False),
   Field('autor',db.auth_user,writable=False,readable=True),
   Field("cantidad", "double", default=0.00,requires=IS_NOT_EMPTY()),
   Field('articulo_id','reference items'),
   format=lambda record: record.articulo_id.descripcion)

#if db(db.items).count() <= 0:
 #   for item in ITEMS:
  #     db.items.insert(descripcion=item[0], marca=item[1],saldo=item[2],
   #                      precio=item[3],medida=item[4])
