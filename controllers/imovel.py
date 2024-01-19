# -*- coding: utf-8 -*-

# Controller de Imóveis

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
    imoveis = db(
        (db.uf.id == db.imovel.uf_id) &
        (db.cidade.id == db.imovel.cidade_id) &
        (db.categoria.id == db.imovel.categoria_id) &
        (db.tipo.id == db.imovel.tipo_id) &
        (db.situacao.id == db.imovel.situacao_id)
    ).select(
        db.imovel.ALL,
        db.cidade.nome,
        db.categoria.nome,
        db.tipo.nome,
        db.situacao.nome,
        db.uf.nome,
        limitby = limitby,
        orderby = db.imovel.descricao)
    return dict(imoveis = imoveis,page = page, items_per_page = items_per_page)

# Adicionar/Alterar cidade
@auth.requires_login()
@auth.requires_membership('corretor')
def insert():
    args = request.args(0)
    sku = None
    if(args == 'new'):
        form = SQLFORM(db.imovel, submit_button = 'Salvar')
    else:
        id = request.args(0, cast = int)
        imo = db.imovel(id)
        sku = imo.sku
        form = SQLFORM(db.imovel, imo, submit_button = 'Salvar')
    if(form.process().accepted):
        if(args == 'new'):
            imovel_id = form.vars.id
            imovel = db.imovel[imovel_id]
            tipo = db.tipo[imovel.tipo_id]
            categoria = db.categoria[imovel.categoria_id]
            sku = str(imovel_id) + tipo.nome[0:3] + categoria.nome[0:3]
            db(db.imovel.id == imovel_id).update(sku = sku)
            session.flash = "Imóvel inserido com sucesso!!!"
            redirect(URL('imovel', 'index'))
        else:
            session.flash = "Imóvel alterado com sucesso!!!"
            redirect(URL('imovel', 'index'))
    if(form.errors):
        response.flash = "Verifique os campos pedidos..."
    return dict(form = form, sku = sku)

# Excluir imovel
@auth.requires_login()
@auth.requires_membership('corretor')
def delete():
    id = request.args(0, cast = int)
    db(db.imovel.id == id).delete()
    session.flash = "Imóvel excluído com sucesso."
    redirect(URL('imovel', 'index'))
    return dict()

# Exibe comodos relacionados ao imóvel
@auth.requires_login()
@auth.requires_membership('corretor')
def comodos():
    imovel_id = int(request.args[0])
    sku = db.imovel[imovel_id].sku
    comodos = db(
        (db.imovel_comodo.imovel_id == imovel_id) &
        (db.comodo.id == db.imovel_comodo.comodo_id)
    ).select(
        db.imovel_comodo.ALL,
        db.comodo.nome)
    return dict(comodos = comodos, sku = sku, imovel_id = imovel_id)

# Inserir Cômodos
@auth.requires_login()
@auth.requires_membership('corretor')
def in_comodos():
    imo_id = request.vars.imovel_id
    com_id = request.vars.comodo_id
    obs = request.vars.observacao
    db.imovel_comodo.insert(imovel_id = imo_id, comodo_id = com_id, observacao = obs)
    session.flash = "Cômodo adicionado com sucesso!!!"
    redirect(URL('imovel', 'comodos/'+imo_id + '/0'))
    return dict()

# Excluir Cômodos
@auth.requires_login()
@auth.requires_membership('corretor')
def exc_comodo():
    id_com = request.args(0, cast = int)
    id_imo = request.args(1, cast = int)
    db(db.imovel_comodo.id == id_com).delete()
    session.flash = "Cômodo excluído com sucesso!!!"
    redirect(URL('imovel', 'comodos/' + str(id_imo) + '/0'))
    return dict()

# Chamada
def servico():
    session.forget()
    return service()

# Pesquisa ajax
@service.json
def search(s = '%'):
    pesquisa = '%' + s + '%'
    result = db(db.comodo.nome.like(pesquisa)).select()
    return result
