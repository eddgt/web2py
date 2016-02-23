# coding: utf8
# intente algo como
def index(): return dict(message="hello from configmenu.py")

def articulos():
    formulario =SQLFORM.smartgrid(db.articulo)
    return locals()

def usuarios():
    formulario =SQLFORM.grid(db.auth_user)
    return locals()

def enviaCorreo():
#mail.send('oulloa@televida.biz',
# 'Asunto del mensaje',
#  '<html><img src="cid:foto" /></html>',
#  attachments = mail.Attachment('/home/eddgt/IMG_03072014_163916.png', content_id='foto'))

        mail.send(to=['edmundo_ulloa@hotmail.com'],
          subject='Test Mail function - Web2Py',
          # If reply_to is omitted, then mail.settings.sender is used
          cc=['edmundoulloa7@gmail.com'],
          message='<html><body><p>Buen día <br> <br> Adjunto les envío reporte "Base usuarios Recargamania Movistar PA 2014" al dia de hoy  <br>  <br> Saludos, <br>  <br>Osman E. Ulloa</p></body> </html>',
    #attachments = mail.Attachment('/home/eddgt/IMG_03072014_163916.png', content_id='foto')),
    attachments = mail.Attachment('/home/eddgt/Documentos/output_cron/suscrip_157/reporte.zip',
                                   content_id='myreport'))
