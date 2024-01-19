# -*- coding: utf-8 -*-
# Controller padrão

@auth.requires_login()
@auth.requires_membership('corretor')
def index():
    sku = request.vars.sku or ''
    if(len(request.args)):
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = 6
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    imoveis = db(
        (db.cidade.id == db.imovel.cidade_id) &
        (db.categoria.id == db.imovel.categoria_id) &
        (db.tipo.id == db.imovel.tipo_id) &
        (db.situacao.id == db.imovel.situacao_id) &
        (db.imovel.sku.like('%' + sku + '%'))
    ).select(
        db.imovel.ALL,
        db.cidade.nome,
        db.categoria.nome,
        db.tipo.nome,
        db.situacao.nome,
        limitby = limitby,
        orderby = db.imovel.sku)
    return dict(imoveis = imoveis,page = page, items_per_page = items_per_page)

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


# Chamada
def servico():
    session.forget()
    return service()

# Pesquisa ajax
@service.json
def search(s = ''):
    pesquisa = '%' + s + '%'
    result = None
    if(len(s) == 0):
        result = []
    else:
        result = db(db.imovel.sku.like(pesquisa)).select(
            db.imovel.sku,
            orderby = db.imovel.sku
        )
    return result
