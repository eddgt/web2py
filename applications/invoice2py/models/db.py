# -*- coding: utf-8 -*-

# invoice2py: an invoice web interface app for web2py
#
# Project page: http://code.google.com/p/ivoice2py
#
#    Copyright (C) 2013 Alan Etkin <spametki@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/
#
#    Developed with web2py, by Massimo Di Pierro

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

# PRODUCTS and CUSTOMERS will be added to the database automatically
# as dummy data

PRODUCTS = [("spamelon", 10.34, "Kg"), ("banana", 32.32, "Kg"),
            ("waterspamelon", 2.32, "Kg"), ("cherry", 32.33, "Kg"),
            ("raspberry", 19.34, "Kg"), ("pear", 23.21, "Kg"),
            ("pineapple", 24.12, "Kg"), ("orange", 12.34, "Kg"),
            ("grapefruit", 10.03, "Kg"), ("tangerine", 20.30, "Kg"),
            ("apple", 02.23, "Kg"), ("fig", 20.24, "Kg"),
            ("kiwi", 10.02, "Kg"), ("strawberry", 20.21, "Kg"),
            ("discount", -1.00, "units"), ("charge", 1.00, "units" )]

CUSTOMERS = [("Michael", "23423084230"), ("John", "320984230984"),
             ("Graham", "234092349"), ("Terry", "23094230"),
             ("Eric", "0923840293")]

# STATUSES indicates wether an invoice can be edited (is open) or
# it is closed. Closed operations can be locked for archive purposes
# or cancelled

STATUSES = {"open": T("Open"), "locked": T("Locked"),
            "cancelled": T("Cancelled")}

PAYMENTS = ["cash", "credit card", "other"]

UNITS = ["units", "Kg", "g", "l"]

# The bill's recipient
db.define_table("customer",
                Field("name"),
                Field("taxpayer"),
                format="%(name)s (%(taxpayer)s)")

# concepts can be articles, discounts or anything that affects the
# amount of the invoice.
db.define_table("concept",
                Field("name"),
                Field("description"),
                Field("amount", "double", default=0.00),
                Field("measure", requires=IS_IN_SET(UNITS),
                      default="units"),
                format="%(name)s: $%(amount)s (%(measure)s)")

db.define_table("invoice",
                Field("created_on", "datetime", default=request.now),
                Field("created_by", "reference auth_user",
                      default=auth.user_id, writable=False),
                Field("customer_id", "reference customer"),
                Field("description"),
                Field("total", "double",
                      writable=False, default=0.00),
                Field("payment", requires=IS_IN_SET(PAYMENTS)),
                Field("status", requires=IS_IN_SET(STATUSES),
                      default="open", writable=False),
                format="%(id)s")

# Each invoice item will be recorded individually. This allows a more
# easy control over the invoice contents, but also requires an extra
# set of records (and a new table) in the database backend.
db.define_table("item",
                Field("invoice_id", "reference invoice",
                      default=session.invoice_id,
                      writable=False),
                Field("concept_id", "reference concept"),
                Field("amount", "double", default=0.00),
                Field("total", "double", default=0.00,
                      writable=False),
                format=lambda record: record.concept_id.name)

# Here we link invoice ids to the invoice details page.
db.invoice.id.represent = lambda id, field: \
    A(id, _href=URL(c="default", f="invoice", args=["invoice", id]))


# Automatically add dummy data (not recommended in production)
if db(db.customer).count() <= 0:
    for customer in CUSTOMERS:
        db.customer.insert(name=customer[0],
                           taxpayer=customer[1])
    for product in PRODUCTS:
       db.concept.insert(name=product[0], amount=product[1],
                         measure=product[2])

# This will be called by the business logic to update open invoices.
# It computes the invoice items and updates the total amounts
def invoice_total(invoice):
    if invoice.status in ("locked", "cancelled"): return
    items = db(db.item.invoice_id==invoice.id).select()
    total = 0.00
    for item in items:
        item_total = item.amount * item.concept_id.amount
        item.update_record(total=item_total)
        total += item_total
    invoice.update_record(total=total)

