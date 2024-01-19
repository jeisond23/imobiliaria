# -*- coding: utf-8 -*-

# Controller de UFs

# Página inícial do controller
@auth.requires_login()
@auth.requires_membership('corretor')
def index():
    if(len(request.args)):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 4
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    ufs = db().select(db.uf.ALL, limitby = limitby, orderby = db.uf.nome)
    return dict(ufs = ufs,page = page, items_per_page = items_per_page)

# Adicionar/Alterar uf
@auth.requires_login()
@auth.requires_membership('corretor')
def insert():
    args = request.args(0)
    if(args == 'new'):
        form = SQLFORM(db.uf, submit_button = 'Salvar')
    else:
        id = request.args(0, cast = int)
        uf = db.uf(id)
        form = SQLFORM(db.uf, uf, submit_button = 'Salvar')
    if(form.process().accepted):
        if(args == 'new'):
            session.flash = "UF inserido com sucesso!!!"
            redirect(URL('uf', 'index'))
        else:
            session.flash = "UF alterado com sucesso!!!"
            redirect(URL('uf', 'index'))
    if(form.errors):
        response.flash = "Verifique os campos pedidos..."
    return dict(form = form)

# Excluir uf
@auth.requires_login()
@auth.requires_membership('corretor')
def delete():
    id = request.args(0, cast = int)
    db(db.uf.id == id).delete()
    session.flash = "UF excluído com sucesso."
    redirect(URL('uf', 'index'))
    return dict()
