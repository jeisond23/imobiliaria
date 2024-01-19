# -*- coding: utf-8 -*-

# Controller de Cidades

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
    cidades = db(db.uf.id == db.cidade.uf_id).select(db.cidade.ALL, db.uf.nome, limitby = limitby, orderby = db.cidade.nome)
    return dict(cidades = cidades,page = page, items_per_page = items_per_page)

# Adicionar/Alterar cidade
@auth.requires_login()
@auth.requires_membership('corretor')
def insert():
    args = request.args(0)
    if(args == 'new'):
        form = SQLFORM(db.cidade, submit_button = 'Salvar')
    else:
        id = request.args(0, cast = int)
        cid = db.cidade(id)
        form = SQLFORM(db.cidade, cid, submit_button = 'Salvar')
    if(form.process().accepted):
        if(args == 'new'):
            session.flash = "Cidade inserida com sucesso!!!"
            redirect(URL('cidade', 'index'))
        else:
            session.flash = "Cidade alterada com sucesso!!!"
            redirect(URL('cidade', 'index'))
    if(form.errors):
        response.flash = "Verifique os campos pedidos..."
    return dict(form = form)

# Excluir cidade
@auth.requires_login()
@auth.requires_membership('corretor')
def delete():
    id = request.args(0, cast = int)
    db(db.cidade.id == id).delete()
    session.flash = "Cidade excluída com sucesso."
    redirect(URL('cidade', 'index'))
    return dict()
