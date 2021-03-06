# coding: utf8
from gluon.scheduler import Scheduler
planificador = Scheduler(db)

def leeArchivo():
    archivo = open('/home/eddgt/Documentos/output_cron/alarmas/revisa_cdc_programacion.txt','r')
    linea = archivo.read()
    if linea == """\n0\n""":

        return dict(mensaje="""Todo ok! en el archivo croneado /home/eddgt/Documentos/output_cron/alarmas/revisa_cdc_programacion.txt,\n
                                Contenido en el archivo: """+linea)
#redirect(URL("http://localhost:8000/hercules/default/enviaSMS"))
    else:
        enviaSMS1()
        enviaSMS2()
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

def enviaSMS1():
    import os
    os.system("wget -U firefox -O sms1.log  http://172.168.1.8:13200/sendsms?username=televida\&password=voiceweb\&from=5028260\&smsc=claro\&dlr-mask=0\&coding=0\&mclass=1\&to=50254656344\&text=Alerta%20Activa%20:%20Revisar%20cdc_programacion%20existen%20registros%20en%20estado%20E%20.")

def enviaSMS2():
    import os
    os.system("wget -U firefox -O sms2.log http://172.168.1.10:13200/sendsms?username=televida\&password=voiceweb\&from=42644194\&smsc=mymodem\&dlr-mask=0\&to=52364478\&text=Alarma%20Activa%20:%20Revisar%20cdc_programacion%20existen%20registros%20en%20estado%20E%20.")

def  smsFallidos():
    import os
    os.system("wget -U firefox -O smsFallidos.log  http://172.168.1.8:13200/sendsms?username=televida\&password=voiceweb\&from=5028260\&smsc=claro\&dlr-mask=0\&coding=0\&mclass=1\&to=50254656344\&text=Alerta%20Activa%20:%Revisar%20be_http_request_response%20existen%20paquetes%20Fallidos!%20.")

def revisaFallidos():
    archivo = open('/home/eddgt/Documentos/output_cron/alarmas/revisa_fallidos_beconnected.txt','r')
    linea = archivo.read()
    if linea == "\n0\n":

        return dict(mensaje="""Todo ok! en el archivo croneado /home/eddgt/Documentos/output_cron/alarmas/revisa_fallidos_beconnected.txt,\n
                                Contenido en el archivo: """+linea)
    else:
        smsFallidos()

def sendReportDigicelSV():
    import datetime

    #format de file name as Digicel requested
    today = datetime.datetime.now()
    dateFormat=today.strftime("%Y%m%d")
    reportToSend='TELEVIDA_'+dateFormat+'.zip'

    #mail parameters
    mail.send(to=['Marcela.Aparicio@digicelgroup.com'],
    subject='Reporte usuarios activos Digicel',
    # If reply_to is omitted, then mail.settings.sender is used
    cc=['mrodriguez@televida.biz','cestrada@televida.biz','soporte247@televida.biz','kperdomo@televida.biz','mdeleon@televida.biz','Carmen.Lazo@digicelgroup.com'],
    message='<html><body><p>Buen día <br> <br> Adjunto envío reporte "Usuarios activos Digicel" al dia de hoy  <br>  <br>Cualquier consulta estamos a la orden,<br> Atte, <br>  <br>Osman E. Ulloa <br>Soporte Regional Televida</p></body> </html>',
    attachments = mail.Attachment('/home/eddgt/Documentos/output_cron/reportes/'+reportToSend,
                                   content_id='myreport'))
def sendReportClaroNi():
        #mail.send(to=['edmundo_ulloa@hotmail.com'],
        mail.send(to=['JJolmedo@televida.biz','cestrada@televida.biz','kperdomo@televida.biz'],
        subject='Reporte Claro NI',
        cc=['soporte247@televida.biz','mdeleon@televida.biz'],
        message='<html><body><p>Buen día <br> <br> Adjunto envío reporte "Detalle Usuarios con cobro en el mes anterior pero no en este mes 2014" generado el dia de hoy  <br>  <br>Cualquier consulta estamos a la orden,<br> Atte. <br>  <br>Osman E. Ulloa <br>Soporte Regional Televida</p></body> </html>',
    attachments = mail.Attachment('/home/eddgt/Documentos/output_cron/reportes/claroni/reporte.zip',
                                   content_id='myreport'))
def sendReportKwClaroNi():
        mail.send(to=['kiglesias@televida.biz'],
        #mail.send(to=[''],
        subject='Reporte Suscritos KW GANA - Claro NI',
        cc=['soporte247@televida.biz'],
        message='<html><body><p>Buen día <br> <br> Adjunto envío reporte "Estado de Usuarios suscritos por medio de KW GANA " correspondiente a la semana pasada generado el dia de hoy  <br>  <br>Cualquier consulta estamos a la orden,<br> Atte. <br>  <br>Osman E. Ulloa <br>Soporte Regional Televida</p></body> </html>',
    attachments = mail.Attachment('/home/eddgt/Documentos/output_cron/reportes/claroni/reporteKwGanaSus239.csv',
                                   content_id='myreport'))

def sendReportActiveUsersMvstrSV():
        #mail.send(to=['edmundo_ulloa@hotmail.com'],
        mail.send(to=['josealberto.calderon@telefonica.com'],
        subject='Reporte Suscritos Megapremios y Back To School',
        #cc=['edmundoulloa7@gmail.com'],
        cc=['mrodriguez@televida.biz', 'dsolombrino@televida.biz', 'cestrada@televida.biz', 'soporte247@televida.biz'],
        message="""<html><body><p>Buen día <br> <br>Se envia el reporte solicitado de Numeros suscritos activos en Megapremios Movistar SV , Back to School Movistar SV y Suscritos en Ambos<br>  <br>Cualquier consulta estamos a la orden,<br> Atte. <br>  <br>Osman E. Ulloa <br>Soporte Regional Televida</p></body> </html>""",
    attachments = mail.Attachment('/home/eddgt/Documentos/output_cron/reportes/movistarsv/reporteActivosMovistarSV.xlsx',
                                   content_id='mvstrReport'))

"""def enviaSMS():
    import os
    os.system("wget -U firefox -O mail.log  http://172.168.1.8:13200/sendsms?username=televida\&password=voiceweb\&from=5028260\&smsc=claro\&dlr-mask=0\&coding=0\&mclass=1\&to=50254656344\&text=Alerta%20Activa%20:%20Revisar%20cdc_programacion%20existen%20registros%20en%20estado%20E%20.")"""
