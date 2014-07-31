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

def conteo():
    session.conteo=(session.conteo or 0)+1
    return dict(conteo=session.conteo, ahora=request.now)

def leeArchivo():
    archivo = open('/home/eddgt/Documentos/output_cron/alarmas/revisa_cdc_programacion.txt','r')
    linea = archivo.read()
    if linea == """\n0\n""":

        return dict(mensaje="""Todo ok! en el archivo croneado /home/eddgt/Documentos/output_cron/alarmas/revisa_cdc_programacion.txt,\n
                                Contenido en el archivo: """+linea)
#redirect(URL("http://localhost:8000/hercules/default/enviaSMS"))
    else:
        enviaSMS()
        enviaCorreo()
        #return dict(mensaje="""Hay un problema en la cdc_programacion,\n
         #                       Contenido en el archivo: """+linea)
def enviaCorreo():
        mail.send(to=['edmundo_ulloa@hotmail.com'],
        subject='Alarma - CDC - Claro CR',
        #cc=['edmundoulloa7@gmail.com'],
        message='<html><body><p>Alarma: <br> <br> Revisar cdc_programacion, existen regisros con estado = E  <br>  <br> <br>Osman E. Ulloa <br>Soporte Regional Televida</p></body> </html>',
    #attachments = mail.Attachment('/home/eddgt/Documentos/output_cron/suscrip_157/reporte.zip',content_id='alarmacdc')
    )

def enviaSMS():
    import os
    os.system("wget -U firefox -O mail.log  http://172.168.1.8:13200/sendsms?username=televida\&password=voiceweb\&from=5028260\&smsc=claro\&dlr-mask=0\&coding=0\&mclass=1\&to=50254656344\&text=Alerta%20Activa%20:%20Revisar%20cdc_programacion%20existen%20registros%20en%20estado%20E%20.")
