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
    response.flash = T("Welcome to my Web Site Powered by web2py!")
    #return dict(message=T('Hello World'))
    return dict(facturas=db().select(db.factura.ALL))
    #agrepado segun tutorial 19052014:15hrs
    #return dict(articulos=db().select(db.articulo.ALL))


#def view_post():
 #   id_articulo = request.args(0)
  #  articulo = db.articulo[id_articulo] or    redirect(URL(r=request,f='index'))
   # if auth.is_logged_in():
    #    db.comentario.articulo.default = articulo.id
     #   db.comentario.autor.default = auth.user.id
      #  form = crud.create(db.comentario)
    #else:
     #   form = A("inicie sesión para        comentar",_href=URL(r=request,f='user/login'))
    #comentarios =    db(db.comentario.articulo==articulo.id).select(db.comentario.ALL)
    #return dict(articulo=articulo, form=form,
    #comentarios=comentarios)

def view_factura():
    id_factura = request.args(0)
    factura = db.factura[id_factura] or redirect(URL(r=request,f='index'))
    if auth.is_logged_in():
        db.item_factura.factura_id.default = factura.id
        db.item_factura.autor.default = auth.user.id
        form = crud.create(db.item_factura)
    else:
        form = A("inicie sesión para agregar items",_href=URL(r=request,f='user/login'))
    facturas_det =    db(db.item_factura.factura_id==factura.id).select(db.item_factura.ALL)
    return dict(factura=factura, form=form,
    facturas_det=facturas_det)






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
