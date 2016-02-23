# coding: utf8
# intente algo como
def index(): return dict(message="hello from autosendmail.py")

def enviaCorreo():
mail.send('oulloa@televida.biz',
  'Asunto del mensaje',
  '<html><img src="cid:foto" /></html>',
  attachments = mail.Attachment('/home/eddgt/IMG_03072014_163916.png', content_id='foto'))
