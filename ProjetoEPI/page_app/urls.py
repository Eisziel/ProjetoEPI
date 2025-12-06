# jj_investimento/urls.py

from django.contrib import admin
from django.urls import path

from page_app.views import (
    # 🌐 Páginas públicas (landing)
    index, contato, services, info,

    # 🔹 Cadastro público de colaboradores (público)
    cadastrar_colaborador, cadastrar_obrigado,

    # 👥 COLABORADORES (área administrativa)
    listar_colaboradores, criar_colaborador, editar_colaborador, excluir_colaborador,

    # 🧍 Usuário do sistema (login estático)
    cadastrar_usuario, entrar, logout_usuario,

    # 🧍 Meu perfil / Configurações / Ajuda
    perfil_usuario, configuracoes_usuario, ajuda_usuario,

    # 🥽 EQUIPAMENTOS
    cadastrar_equipamento, listar_equipamentos,
    editar_equipamento, excluir_equipamento,

    # 📝 CONTROLE DE EPIs
    controlar_epi, editar_controle_epi, excluir_controle_epi,

    # 📊 RELATÓRIOS
    relatorio_colaborador,

    # 🔐 Login administrativo real (Django)
    login_admin, logout_admin,
)

urlpatterns = [
    # -----------------------------------------
    # ⚙️ Admin Django
    # -----------------------------------------
    path('admin/', admin.site.urls),

    # -----------------------------------------
    # 🌐 Páginas públicas
    # -----------------------------------------
    path('', index, name='index'),
    path('contato/', contato, name='contato'),
    path('services/', services, name='services'),
    path('info/', info, name='info'),

    # -----------------------------------------
    # 👤 Usuário do sistema (login ESTÁTICO)
    # -----------------------------------------
    path('usuarios/novo/', cadastrar_usuario, name='cadastrar_usuario'),
    path('entrar/', entrar, name='entrar'),
    path('logout/', logout_usuario, name='logout_usuario'),

    # -----------------------------------------
    # 👤 Perfil / Configurações / Ajuda
    # -----------------------------------------
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('configuracoes/', configuracoes_usuario, name='configuracoes_usuario'),
    path('ajuda/', ajuda_usuario, name='ajuda_usuario'),

    # -----------------------------------------
    # 🔐 Login administrativo REAL (User do Django)
    # -----------------------------------------
    path('login/', login_admin, name='login'),
    path('logout-admin/', logout_admin, name='logout_admin'),

    # -----------------------------------------
    # 🟢 Cadastro público de Colaborador
    # -----------------------------------------
    path('cadastrar/', cadastrar_colaborador, name='cadastrar_colaborador'),
    path('cadastrar/obrigado/', cadastrar_obrigado, name='cadastrar_obrigado'),

    # -----------------------------------------
    # 👨‍💼 COLABORADORES
    # -----------------------------------------
    path('colaboradores/', listar_colaboradores, name='listar_colaboradores'),
    path('colaboradores/novo/', criar_colaborador, name='criar_colaborador'),
    path('colaboradores/editar/<int:id>/', editar_colaborador, name='editar_colaborador'),
    path('colaboradores/excluir/<int:id>/', excluir_colaborador, name='excluir_colaborador'),

    # -----------------------------------------
    # 🥽 EQUIPAMENTOS
    # -----------------------------------------
    path('equipamentos/', listar_equipamentos, name='listar_equipamentos'),
    path('equipamentos/novo/', cadastrar_equipamento, name='cadastrar_equipamento'),
    path('equipamentos/editar/<int:id>/', editar_equipamento, name='editar_equipamento'),
    path('equipamentos/excluir/<int:id>/', excluir_equipamento, name='excluir_equipamento'),

    # -----------------------------------------
    # 📋 CONTROLE DE EPI
    # -----------------------------------------
    path('epi/controlar/', controlar_epi, name='controlar_epi'),
    path('epi/editar/<int:id>/', editar_controle_epi, name='editar_controle_epi'),
    path('epi/excluir/<int:id>/', excluir_controle_epi, name='excluir_controle_epi'),

    # -----------------------------------------
    # 📊 RELATÓRIOS
    # -----------------------------------------
    path('relatorios/colaborador/', relatorio_colaborador, name='relatorio_colaborador'),
]
