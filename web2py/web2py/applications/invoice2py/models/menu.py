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

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
                  _class="brand",_href="http://www.web2py.com/")
response.title = request.application.replace('_',' ').title()
response.subtitle = T('A simple online invoice interface')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Alan Etkin <spametki@gmail.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework, invoice'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('My invoices'), False, URL('default', 'index'), [])
]

DEVELOPMENT_MENU = False

INVOICE_ID = session.invoice_id
if request.args(0) == "invoice":
    INVOICE_ID = request.args(1)

# Invoice menu. It gives acces to:
#    - header CRUD (shows the current invoice id)
#    - details (items CRUD)
#    - close (set as complete)/cancel/clear invoice actions

response.menu += [(T("Invoice No. %(number)s") % \
                   dict(number=INVOICE_ID or 
                        "(%s)" % T("Create")), True,
                        URL(c="default", f="invoice")),
                  (T("Invoice details"), True,
                   URL(c="default", f="details"))]

if INVOICE_ID: response.menu += [(T("Clear"), True, URL(c="default",
    f="status", args=["invoice", "none", "status", "clear"])),]

if "auth" in locals(): auth.wikimenu()

