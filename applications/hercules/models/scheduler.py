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

"""def enviaSMS():
    import os
    os.system("wget -U firefox -O mail.log  http://172.168.1.8:13200/sendsms?username=televida\&password=voiceweb\&from=5028260\&smsc=claro\&dlr-mask=0\&coding=0\&mclass=1\&to=50254656344\&text=Alerta%20Activa%20:%20Revisar%20cdc_programacion%20existen%20registros%20en%20estado%20E%20.")"""
