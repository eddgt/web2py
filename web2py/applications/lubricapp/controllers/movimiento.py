# coding: utf8
# intente algo como
def index(): return dict(message="hello from movimiento.py")

@auth.requires_login()
def movimientos():
    #formulario =SQLFORM.smartgrid(db.movimiento)#smartgrid= muestra los detalles del movimiento por medio de link
    formulario =SQLFORM.grid(db.movimiento)
    return locals()
