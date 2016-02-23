# coding: utf8
# intente algo como
def index(): return dict(message="hello from articulo.py")

@auth.requires_login()
def articulos():
    formulario =SQLFORM.grid(db.articulo)
    return locals()
