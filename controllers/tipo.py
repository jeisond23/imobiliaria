# -*- coding: utf-8 -*-

# Controller de Tipo

# Página inicial
@auth.requires_login()
@auth.requires_membership('corretor')
def index():
    if(len(request.args)):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 4
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    tipos = db().select(db.tipo.ALL, limitby = limitby, orderby = db.tipo.nome)
    return dict(tipos = tipos,page = page, items_per_page = items_per_page)

# Adicionar/Alterar tipo
@auth.requires_login()
@auth.requires_membership('corretor')
def insert():
    args = request.args(0)
    if(args == 'new'):
        form = SQLFORM(db.tipo, submit_button = 'Salvar')
    else:
        id = request.args(0, cast = int)
        tip = db.tipo(id)
        form = SQLFORM(db.tipo, tip, submit_button = 'Salvar')
    if(form.process().accepted):
        if(args == 'new'):
            session.flash = "Tipo inserida com sucesso!!!"
            redirect(URL('tipo', 'index'))
        else:
            session.flash = "Tipo alterada com sucesso!!!"
            redirect(URL('tipo', 'index'))
    if(form.errors):
        response.flash = "Verifique os campos pedidos..."
    return dict(form = form)

# Excluir tipo
@auth.requires_login()
@auth.requires_membership('corretor')
def delete():
    id = request.args(0, cast = int)
    db(db.tipo.id == id).delete()
    response.flash = "Categoria excluída com sucesso."
    redirect(URL('tipo', 'index'))
    return dict()
