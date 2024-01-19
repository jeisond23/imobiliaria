# -*- coding: utf-8 -*-

# Controller de Categorias

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
    categorias = db().select(db.categoria.ALL, limitby = limitby, orderby = db.categoria.nome)
    return dict(categorias = categorias,page = page, items_per_page = items_per_page)

# Adicionar/Alterar categoria
@auth.requires_login()
@auth.requires_membership('corretor')
def insert():
    args = request.args(0)
    if(args == 'new'):
        form = SQLFORM(db.categoria, submit_button = 'Salvar')
    else:
        id = request.args(0, cast = int)
        cat = db.categoria(id)
        form = SQLFORM(db.categoria, cat, submit_button = 'Salvar')
    if(form.process().accepted):
        if(args == 'new'):
            session.flash = "Categoria inserida com sucesso!!!"
            redirect(URL('categoria', 'index'))
        else:
            session.flash = "Categoria alterada com sucesso!!!"
            redirect(URL('categoria', 'index'))
    if(form.errors):
        response.flash = "Verifique os campos pedidos..."
    return dict(form = form)

# Excluir categoria
@auth.requires_login()
@auth.requires_membership('corretor')
def delete():
    id = request.args(0, cast = int)
    db(db.categoria.id == id).delete()
    response.flash = "Categoria excluída com sucesso."
    redirect(URL('categoria', 'index'))
    return dict()
