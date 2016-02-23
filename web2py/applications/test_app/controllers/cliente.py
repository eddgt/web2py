# coding: utf8
# intente algo como
def index(): return dict(message="hello from cliente.py")

def clientes():
    formulario =SQLFORM.smartgrid(db.cliente)
    return locals()

#def report_form():
#    form = plugin_appreport.REPORTFORM(table=db.cliente)
#    return dict(form = form)
