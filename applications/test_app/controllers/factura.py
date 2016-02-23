# coding: utf8
# intente algo como
def index(): return dict(message="hello from factura.py")

#declarar la funcion que se llamara desde el menu.py
def facturas():
    formulario =SQLFORM.grid(db.factura)
    return locals()
