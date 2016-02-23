# coding: utf8
# intente algo como
def index(): return dict(message="hello from configmenu.py")

def articulos():
    formulario =SQLFORM.smartgrid(db.articulo)
    return locals()

def usuarios():
    formulario =SQLFORM.grid(db.auth_user)
    return locals()
