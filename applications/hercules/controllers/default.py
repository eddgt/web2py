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

def enviaSMS2():
    import os
    os.system("wget -U firefox -O sms2.log http://172.168.1.10:13200/sendsms?username=televida\&password=voiceweb\&from=42644194\&smsc=mymodem\&dlr-mask=0\&to=52364478\&text=Alarma%20Activa%20:%20Revisar%20cdc_programacion%20existen%20registros%20en%20estado%20E%20.")

def  smsFallidos():
    import os
    os.system("wget -U firefox -O smsFallidos.log  http://172.168.1.8:13200/sendsms?username=televida\&password=voiceweb\&from=5028260\&smsc=claro\&dlr-mask=0\&coding=0\&mclass=1\&to=50254656344\&text=Alerta%20Activa%20:%Revisar%20be_http_request_response%20existen%20paquetes%20Fallidos!%20.")

    """os.system("wget -U firefox -O smsFallidos.log http://172.168.1.10:13200/sendsms?username=televida\&password=voiceweb\&from=42644194\&smsc=mymodem\&dlr-mask=0\&to=54656344\&text='Alarma Activa -  Se encontraron paquetes fallids en be_http_request_response de Apolo'")"""

def revisaFallidos():
    archivo = open('/home/eddgt/Documentos/output_cron/alarmas/revisa_fallidos_beconnected.txt','r')
    linea = archivo.read()

    if linea == """\n0\n""":
        return dict(mensaje="""Todo ok! en el archivo croneado /home/eddgt/Documentos/output_cron/alarmas/revisa_fallidos_beconnected.txt,\n
                                Contenido en el archivo: """+linea)
    else:
        smsFallidos()
        return dict(mensaje="""resultado archivo croneado /home/eddgt/Documentos/output_cron/alarmas/revisa_fallidos_beconnected.txt,\n
                                Contenido en el archivo: """+linea)

def sendReportDigicelSV():
    import datetime
    today = datetime.datetime.now()
    dateFormat=today.strftime("%Y%m%d")
    #reportToSend='TELEVIDA_'+dateFormat+'.zip'
    reportToSend='reporte.zip'

    lineas = len(open('/home/eddgt/Documentos/output_cron/reportes/claroni/reporte.csv').readlines())

    if lineas>30000:
        print "envio reporte, tiene "+str(lineas)+" lineas"

        #mail parameters
        mail.send(to=['edmundo_ulloa@hotmail.com'],
        #mail.send(to=['Saribels.Sanjur@telefonica.com'],
        subject='Test-Reporte usuarios activos Digicel',
        # If reply_to is omitted, then mail.settings.sender is used
        #cc=['edmundoulloa7@gmail.com','soporte247@televida.biz'],
        #cc=['clientes.pa@televida.biz','scuchillas@televida.biz','msamayoa@televida.biz','dcamacho@televida.biz','soporte247@televida.biz'],
        message='<html><body><p>Buen día <br> <br> Adjunto envío reporte "Usuarios activos Digicel " al dia de hoy  <br>  <br>Cualquier consulta estamos a la orden,<br> Atte, <br>  <br>Osman E. Ulloa <br>Soporte Regional Televida</p></body> </html>'+str(lineas),
        attachments = mail.Attachment('/home/eddgt/Documentos/output_cron/reportes/claroni/'+reportToSend,
                                   content_id='myreport'))
        return dict(mensaje="""report sent with: """+str(lineas)+" lineas")
    else:
        return dict(mensaje="""report dont sent with: """+str(lineas)+" lineas "+str(today))
    pass

def sendReportKwClaroNi():
        mail.send(to=['oulloa@televida.biz'],
        #mail.send(to=[''],
        subject='Test - Reporte Suscritos KW GANA - Claro NI',
        cc=['soporte247@televida.biz'],
        message='<html><body><p>Buen día <br> <br> Adjunto envío reporte "Estado de Usuarios suscritos por medio de KW GANA " correspondiente a la semana pasada generado el dia de hoy  <br>  <br>Cualquier consulta estamos a la orden,<br> Atte. <br>  <br>Osman E. Ulloa <br>Soporte Regional Televida</p></body> </html>',
    attachments = mail.Attachment('/home/eddgt/Documentos/output_cron/reportes/claroni/reporteKwGanaSus239.csv',
                                   content_id='myreport'))

def sendReportActiveUsersMvstrSV():
        mail.send(to=['edmundo_ulloa@hotmail.com'],
        #mail.send(to=['josealberto.calderon@telefonica.com'],
        subject='Reporte Suscritos Megapremios y Back To School',
        cc=['edmundoulloa7@gmail.com'],
        #cc=['mrodriguez@televida.biz', 'dsolombrino@televida.biz', 'cestrada@televida.biz', 'slima@televida.biz'],
        message="""<html><body><p>Buen día <br> <br>Se envia el reporte solicitado de Numeros suscritos activos en Megapremios Movistar SV , Back to School Movistar SV y Suscritos en Ambos<br>  <br>Cualquier consulta estamos a la orden,<br> Atte. <br>  <br>Osman E. Ulloa <br>Soporte Regional Televida</p></body> </html>""",
    attachments = mail.Attachment('/home/eddgt/Documentos/output_cron/reportes/movistarsv/reporteActivosMovistarSV.xlsx',
                                   content_id='mvstrReport'))

def myScheduler():
    formulario =SQLFORM.smartgrid(db.scheduler_task)
    return locals()
