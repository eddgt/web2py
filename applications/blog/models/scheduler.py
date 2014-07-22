# coding: utf8
from gluon.scheduler import Scheduler
planificador = Scheduler(db)

def enviaCorreo():

        #mail.send(to=['edmundo_ulloa@hotmail.com'],
        mail.send(to=['Saribels.Sanjur@telefonica.com'],
         subject='Reporte base de usuarios Recargamania PA 2014',
         # If reply_to is omitted, then mail.settings.sender is used
         #cc=['edmundoulloa7@gmail.com'],
        cc=['clientes.pa@televida.biz','scuchillas@televida.biz','msamayoa@televida.biz','dcamacho@televida.biz','soporte247@televida.biz'],
          message='<html><body><p>Buen día <br> <br> Adjunto les envío reporte "Base usuarios Recargamania Movistar PA 2014" al dia de hoy  <br>  <br> Saludos, <br>  <br>Osman E. Ulloa <br>Soporte Regional Televida</p></body> </html>',
    attachments = mail.Attachment('/home/eddgt/Documentos/output_cron/suscrip_157/reporte.zip',
                                   content_id='myreport'))
