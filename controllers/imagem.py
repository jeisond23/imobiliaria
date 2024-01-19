# -*- coding: utf-8 -*-

# Controller de Imagens

@auth.requires_login()
@auth.requires_membership('corretor')
def index():
    acao = "new"
    image = None
    imovel_id = request.args(0, cast = int)
    sku = db.imovel[imovel_id].sku
    imagens = db(db.imagem.imovel_id == imovel_id).select(db.imagem.ALL)
    if(request.args(1) == "edit"):
        acao = "edit"
        image = db(db.imagem.id == request.args(2, cast = int)).select(
            db.imagem.id,
            db.imagem.descricao,
            db.imagem.alt,
            db.imagem.title
        ).first()
    return dict(imagens = imagens, sku = sku, imovel_id = imovel_id, acao = acao, image = image)

# Inserir Imagens
@auth.requires_login()
@auth.requires_membership('corretor')
def in_imagem():
    image = db.imagem.src.store(request.vars.src, request.vars.src)
    imagem = {
        'descricao': request.vars.descricao,
        'alt': request.vars.alt,
        'title': request.vars.title,
        'src': image,
        'imovel_id': request.vars.imovel_id
    }
    db['imagem'].insert(**imagem)
    session.flash = "Imagem salva com sucesso!!!"
    redirect(URL('imagem', 'index/' + request.vars.imovel_id))
    return dict()

# Editar Imagens
@auth.requires_login()
@auth.requires_membership('corretor')
def edit_imagem():
    id = request.args(0, cast = int)
    imagem = {
        'descricao': request.vars.descricao,
        'alt': request.vars.alt,
        'title': request.vars.title,
        'imovel_id': request.vars.imovel_id
    }
    db(db.imagem.id == id).update(**imagem)
    session.flash = "Imagem alterada com sucesso!!!"
    redirect(URL('imagem', 'index/' + request.vars.imovel_id))
    return dict()

# Excluir Imagem
@auth.requires_login()
@auth.requires_membership('corretor')
def exc_image():
    imovel_id = request.args(1)
    image_id = request.args(0, cast = int)
    name = db.imagem[image_id].title
    db(db.imagem.id == image_id).delete()
    session.flash = "Imagem de " + name + " excluída com sucesso!!!"
    redirect(URL('imagem', 'index/' + imovel_id))
    return dict()

@cache.action()
def download():
    return response.download(request, db)
