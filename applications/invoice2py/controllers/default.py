# -*- coding: utf-8 -*-

# invoice2py: an invoice web interface app for web2py
#
# Project page: http://code.google.com/p/ivoice2py
#
#    Copyright (C) 2013 Alan Etkin <spametki@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/
#
#    Developed with web2py, by Massimo Di Pierro

@auth.requires_login()
def index():
    """
    First page. Show the list (grid) of available invoices
    """
    return dict(table=SQLFORM.grid(db.invoice,
                create=False, editable=False, deletable=False))

@auth.requires_login()
def status():
    """ This is command action to update the invoice status.

    It is triggered by the other menu actions.

    commands:
        - clear: resets the invoice selection
          (allows to create a new one)
        - lock: close the invoice avoiding further modifications
        (for supporting billing)
        - cancel: abort the current invoice
    """
    if not request.args[3] == "clear":
        invoice = db.invoice[request.args[1]]
        if invoice:
            invoice.update_record(status=request.args[3])
            session.flash = \
                T("Invoice %(invoice_id)s is %(status)s") % \
                dict(status=request.args[3],
                     invoice_id=request.args[1])
    session.invoice_id = None
    redirect(URL(f="index"))

@auth.requires_login()
def invoice():
    """ The invoice header action

    It allows to create or modify an invoice header.
    Locked or cancelled operations are not editable.
    """
    invoice = customer = readonly = None

    # INVOICE_ID stores the currently selected invoice
    if INVOICE_ID:
        if request.args(1):
            session.invoice_id = request.args(1)
        # get the invoice db record
        invoice = db.invoice[session.invoice_id]

        # compute/update totals for each item and
        # the invoice's total amount
        if invoice: invoice_total(invoice)

        # was this invoice closed? then disable editing
        readonly = invoice.status in ("locked", "cancelled")
        form = SQLFORM(db.invoice, session.invoice_id,
                       readonly=readonly)

        # on invoice update disable editing too (you can keep
        # updating by accessing the invoice header trough the menu)
        if form.process().accepted:
            response.flash = T("Done!")
            form = SQLFORM(db.invoice, session.invoice_id,
                           readonly=True)
        else:
            # here we add the cancel and close (lock) actions to
            # the menu.
            if not readonly:
                response.menu += [
                    (T("Close"), True, URL(f="status",
                     args=["invoice", session.invoice_id,
                           "status", "locked"])),
                    (T("Cancel"), True, URL(f="status",
                     args=["invoice", session.invoice_id,
                           "status", "cancelled"]))]
    else:
        # when there's no invoice informed (by session variable or
        # action argument) we expose a create form
        form = SQLFORM(db.invoice)
        if form.process().accepted:
            session.invoice_id = form.vars.id
            session.flash = T("New invoice created")
            # on sucess, self-redirect to allow editing
            redirect(URL(f="invoice"))
    return dict(form=form)

@auth.requires_login()
def details():
    """
    The invoice details grid.

    It exposes an invoice item CRUD interface and updates totals for
    each submission. It requires a session invoice variable which
    is set by user input (via the menu), so you cannot edit details
    unless you selected an invoice previously.
    """

    if not session.invoice_id:
        # return an empty page if there's no invoice selected
        response.flash = T("No invoice selected!")
        return dict(header=None, details=None)
    else:
        # get the invoice database record
        invoice = db.invoice[session.invoice_id]
        # update item and invoice totals (only open invoices)
        invoice_total(invoice)
        # is the invoice editable? then allow item CRUD.
        editable = not invoice.status in ("locked", "cancelled")
    details = SQLFORM.grid(db.item.invoice_id==session.invoice_id,
        create=editable, editable=editable, deletable=editable)

    # we add the invoice header to the action data for reference
    header = SQLFORM(db.invoice, session.invoice_id, readonly=True)
    return dict(header=header, details=details)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
