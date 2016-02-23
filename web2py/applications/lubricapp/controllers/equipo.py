# coding: utf8
# intente algo como
def index(): return dict(message="hello from equipo.py")

def equipos():
    formulario =SQLFORM.grid(db.equipo)
    return locals()
