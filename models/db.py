# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# Trabalhar com Serviços

from gluon.tools import Service

service = Service()

# Recursos do OS
import os

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = []
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)

# Tabelas do site valenteimoveis.rio.br

db.define_table('categoria', Field('nome', length = 30, unique = True), format = '%(nome)s')

db.define_table('tipo', Field('nome'), format = '%(nome)s')

db.define_table('situacao', Field('nome', unique = True), format = '%(nome)s')

db.define_table('uf', Field('nome', length=2), format = '%(nome)s')

db.define_table('cidade',
                Field('nome'),
                Field('uf_id', 'reference uf'),
                format = '%(nome)s'
)

db.define_table('imovel',
                Field('sku', length=120),
                Field('endereco', length=120),
                Field('bairro', length=40),
                Field('descricao', 'text'),
                Field('capa', 'upload', uploadfolder = os.path.join(request.folder, 'uploads/imoveis'), autodelete = True),
                Field('cidade_id', 'reference cidade'),
                Field('uf_id', 'reference uf'),
                Field('categoria_id', 'reference categoria'),
                Field('situacao_id', 'reference situacao'),
                Field('tipo_id', 'reference tipo'),
                Field('valor', length=15),
                format = '%(sku)s'
)

db.define_table('comodo',
                Field('nome'),
                # Field('descricao', 'text', length=120),
                format = '%(nome)s'
)

db.define_table('imovel_comodo',
                Field('imovel_id', 'reference imovel', ondelete = 'CASCADE'),
                Field('comodo_id', 'reference comodo'),
                Field('observacao', 'text')
)

db.define_table('imagem',
                Field('descricao', length = 120),
                Field('alt'),
                Field('title'),
                # Field('capa', 'boolean'),
                Field('src', 'upload', uploadfolder = os.path.join(request.folder, 'uploads/imoveis'), autodelete = True),
                Field('imovel_id', 'reference imovel')
)

# Validacao das tabelas

## Validacao de Categoria
db.categoria.nome.requires = IS_NOT_IN_DB(db, db.categoria.nome, error_message="O nome ja existe ou o campo está vazio!!!")

## Validacao de Comodo
db.comodo.nome.requires = IS_NOT_IN_DB(db, db.comodo.nome, error_message="O nome ja existe ou o campo está vazio!!!")

## Validacao de Situacao
db.situacao.nome.requires = IS_NOT_IN_DB(db, db.situacao.nome, error_message="O nome ja existe ou o campo está vazio!!!")

## Validacao de Tipo
db.tipo.nome.requires = IS_NOT_IN_DB(db, db.tipo.nome, error_message="O nome ja existe ou o campo está vazio!!!")

## Validacao de UF
db.uf.nome.requires = IS_NOT_IN_DB(db, db.uf.nome, error_message="O nome ja existe ou o campo está vazio!!!")

## Validacao de Cidade
db.cidade.nome.requires = IS_NOT_EMPTY(error_message="Preencha o campo!!!")
db.cidade.uf_id.requires = IS_IN_DB(db, db.uf.id, '%(nome)s', error_message="O nome ja existe ou o campo está vazio!!!")

## Validacao de Imovel
# db.imovel.sku.requires = IS_NOT_IN_DB(db, db.imovel.sku, error_message="O nome ja existe ou o campo está vazio!!!")
db.imovel.endereco.requires = IS_NOT_EMPTY(error_message= "Campo obrigatório!!!!")
db.imovel.bairro.requires = IS_NOT_EMPTY(error_message= "Campo obrigatório!!!!")
db.imovel.descricao.requires = IS_NOT_EMPTY(error_message= "Campo obrigatório!!!!")
db.imovel.valor.requires = IS_NOT_EMPTY(error_message= "Campo obrigatório!!!!")
db.imovel.cidade_id.requires = IS_IN_DB(db, db.cidade.id, '%(nome)s', error_message= "O nome ja existe ou o campo está vazio!!!")
db.imovel.categoria_id.requires = IS_IN_DB(db, db.categoria.id, '%(nome)s', error_message= "O nome ja existe ou o campo está vazio!!!")
db.imovel.situacao_id.requires = IS_IN_DB(db, db.situacao.id, '%(nome)s', error_message = "O nome ja existe ou o campo está vazio!!!")
db.imovel.tipo_id.requires = IS_IN_DB(db, db.tipo.id, '%(nome)s', error_message="Preencha o campo!!!")

## Validacao de imagem
db.imagem.descricao.requires = IS_NOT_EMPTY(error_message= "Campo obrigatório!!!!")
db.imagem.alt.requires = IS_NOT_EMPTY(error_message= "Campo obrigatório!!!!")
db.imagem.title.requires = IS_NOT_EMPTY(error_message= "Campo obrigatório!!!!")
db.imagem.src.requires = IS_NOT_EMPTY(error_message= "Campo obrigatório!!!!")
db.imagem.imovel_id.writable = db.imagem.imovel_id.readable = False

## Validacao de Imovel-Comodo
db.imovel_comodo.imovel_id.requires = IS_IN_DB(db, db.imovel.id, '%(sku)s', error_message = "O nome ja existe ou o campo está vazio!!!")
db.imovel_comodo.comodo_id.requires = IS_IN_DB(db, db.comodo.id, '%(nome)s', error_message = "O nome ja existe ou o campo está vazio!!!")
db.imovel_comodo.observacao.requires = IS_NOT_EMPTY(error_message= "Campo obrigatório!!!!")
