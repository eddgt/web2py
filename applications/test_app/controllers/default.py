# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))

    return dict(table=SQLFORM.grid(db.factura,
                create=False, editable=False, deletable=False))

@auth.requires_login()
def status():
    """ This is command action to update the invoice status.

    It is triggered by the other menu actions.

    commands:
        - clear: resets the invoice selection
          (allows to create a new one)
        - lock: close the invoice avoiding further modifications
        (for supporting billing)
        - cancel: abort the current invoice
    """
    if not request.args[3] == "limpiar":
        factura = db.factura[request.args[1]]
        if factura:
            factura.update_record(status=request.args[3])
            session.flash = \
                T("Factura %(factura_id)s is %(status)s") % \
                dict(status=request.args[3],
                     factura_id=request.args[1])
    session.factura_id = None
    redirect(URL(f="index"))

@auth.requires_login()
def factura():
    """ The invoice header action

    It allows to create or modify an invoice header.
    Locked or cancelled operations are not editable.
    """
    factura = cliente = readonly = None

    # INVOICE_ID stores the currently selected invoice
    if FACTURA_ID:
        if request.args(1):
            session.factura_id = request.args(1)
        # get the invoice db record
        factura = db.factura[session.factura_id]

        # compute/update totals for each item and
        # the invoice's total amount
        if factura: factura_total(factura)

        # was this invoice closed? then disable editing
        readonly = factura.status in ("bloqueada", "cancelada")
        form = SQLFORM(db.factura, session.factura_id,
                       readonly=readonly)

        # on invoice update disable editing too (you can keep
        # updating by accessing the invoice header trough the menu)
        if form.process().accepted:
            response.flash = T("Done!")
            form = SQLFORM(db.factura, session.factura_id,
                           readonly=True)
        else:
            # here we add the cancel and close (lock) actions to
            # the menu.
            if not readonly:
                response.menu += [
                    (T("Close"), True, URL(f="status",
                     args=["factura", session.factura_id,
                           "status", "bloqueada"])),
                    (T("Cancel"), True, URL(f="status",
                     args=["factura", session.factura_id,
                           "status", "cancelada"]))]
    else:
        # when there's no invoice informed (by session variable or
        # action argument) we expose a create form
        form = SQLFORM(db.factura)
        if form.process().accepted:
            session.factura_id = form.vars.id
            session.flash = T("New invoice created")
            # on sucess, self-redirect to allow editing
            redirect(URL(f="factura"))
    return dict(form=form)

@auth.requires_login()
def detalle():
    """
    The invoice details grid.

    It exposes an invoice item CRUD interface and updates totals for
    each submission. It requires a session invoice variable which
    is set by user input (via the menu), so you cannot edit details
    unless you selected an invoice previously.
    """

    if not session.factura_id:
        # return an empty page if there's no invoice selected
        response.flash = T("No invoice selected!")
        return dict(header=None, details=None)
    else:
        # get the invoice database record
        factura = db.factura[session.factura_id]
        # update item and invoice totals (only open invoices)
        factura_total(factura)
        # is the invoice editable? then allow item CRUD.
        editable = not factura.status in ("bloqueada", "cancelada")
    detalle = SQLFORM.grid(db.item.factura_id==session.factura_id,
        create=editable, editable=editable, deletable=editable)

    # we add the invoice header to the action data for reference
    header = SQLFORM(db.factura, session.factura_id, readonly=True)
    return dict(header=header, detalle=detalle)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())


#def person():
 #   person = person = readonly = None
#
#    if not readonly:
#    response.menu +=    (T('Home'), False, URL('default', 'report'), [])
#
#    else:
#        form = SQLFORM(db.factura)
#        redirect(URL(f="person","persons"))
#        return dict(form=form)

#implementacion de appreport plugin
def report():
    form = plugin_appreport.REPORTFORM(person)

    if form.accepts(request.vars, session):
        return plugin_appreport.REPORTPISA(table = person, title = 'List of persons', filter = dict(form.vars))

    return dict(form = form)
