# -*- coding: utf-8 -*-

# Controller de Situações

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
    situacoes = db().select(db.situacao.ALL, limitby = limitby, orderby = db.situacao.nome)
    return dict(situacoes = situacoes,page = page, items_per_page = items_per_page)

# Adicionar/Alterar situacao
@auth.requires_login()
@auth.requires_membership('corretor')
def insert():
    args = request.args(0)
    if(args == 'new'):
        form = SQLFORM(db.situacao, submit_button = 'Salvar')
    else:
        id = request.args(0, cast = int)
        sit = db.situacao(id)
        form = SQLFORM(db.situacao, sit, submit_button = 'Salvar')
    if(form.process().accepted):
        if(args == 'new'):
            session.flash = "Situação inserida com sucesso!!!"
            redirect(URL('situacao', 'index'))
        else:
            session.flash = "Situação alterada com sucesso!!!"
            redirect(URL('situacao', 'index'))
    if(form.errors):
        response.flash = "Verifique os campos pedidos..."
    return dict(form = form)

# Excluir situação
@auth.requires_login()
@auth.requires_membership('corretor')
def delete():
    id = request.args(0, cast = int)
    db(db.situacao.id == id).delete()
    session.flash = "Situação excluída com sucesso."
    redirect(URL('situacao', 'index'))
    return dict()
