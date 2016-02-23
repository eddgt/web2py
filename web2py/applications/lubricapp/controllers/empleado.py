# coding: utf8
# intente algo como
def index(): return dict(message="hello from empleado.py")

@auth.requires_login()
def empleados():
    formulario =SQLFORM.grid(db.empleado)
    return locals()
