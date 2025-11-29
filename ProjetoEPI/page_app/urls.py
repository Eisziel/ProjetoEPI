from django.contrib import admin
from django.urls import path

from page_app.views import (
    # 🌐 Páginas públicas
    index, contato, services, info,

    # 🟢 Cadastro público de conta (visitante)
    cadastrar_colaborador, cadastrar_obrigado,

    # 👤 Usuário do sistema (login simples via sessão)
    cadastrar_usuario, entrar, logout_usuario,
    perfil_usuario, configuracoes_usuario, ajuda_usuario,

    # 👨‍💼 COLABORADORES (área administrativa)
    listar_colaboradores, criar_colaborador, editar_colaborador, excluir_colaborador,

    # 🥽 EQUIPAMENTOS
    cadastrar_equipamento, listar_equipamentos,
    editar_equipamento, excluir_equipamento,

    # 📋 CONTROLE DE EPI
    controlar_epi,

    # 📊 RELATÓRIO
    relatorio_colaborador,

    # 🔐 Login administrativo Django
    login_admin, logout_admin,
)

urlpatterns = [
    # -----------------------------------------
    # ⚙️ Admin Django
    # -----------------------------------------
    path("admin/", admin.site.urls),

    # -----------------------------------------
    # 🌐 Páginas públicas / marketing
    # -----------------------------------------
    path("", index, name="index"),
    path("contato/", contato, name="contato"),
    path("services/", services, name="services"),
    path("info/", info, name="info"),

    # -----------------------------------------
    # 👤 Usuário do sistema (login simples via sessão)
    # -----------------------------------------
    path("usuarios/novo/", cadastrar_usuario, name="cadastrar_usuario"),
    path("entrar/", entrar, name="entrar"),
    path("sair/", logout_usuario, name="logout_usuario"),

    # Perfil / Config / Ajuda
    path("perfil/", perfil_usuario, name="perfil_usuario"),
    path("configuracoes/", configuracoes_usuario, name="configuracoes_usuario"),
    path("ajuda/", ajuda_usuario, name="ajuda_usuario"),

    # -----------------------------------------
    # 🔐 Login administrativo REAL (Django)
    # -----------------------------------------
    path("login/", login_admin, name="login"),
    path("logout-admin/", logout_admin, name="logout_admin"),

    # -----------------------------------------
    # 🟢 Cadastro público de Colaborador (visitante)
    # -----------------------------------------
    path("cadastrar/", cadastrar_colaborador, name="cadastrar_colaborador"),
    path("cadastrar/obrigado/", cadastrar_obrigado, name="cadastrar_obrigado"),

    # -----------------------------------------
    # 👨‍💼 COLABORADORES — Área administrativa
    # -----------------------------------------
    path("colaboradores/", listar_colaboradores, name="listar_colaboradores"),
    path("colaboradores/novo/", criar_colaborador, name="criar_colaborador"),
    path("colaboradores/editar/<int:id>/", editar_colaborador, name="editar_colaborador"),
    path("colaboradores/excluir/<int:id>/", excluir_colaborador, name="excluir_colaborador"),

    # -----------------------------------------
    # 🥽 EQUIPAMENTOS — Área administrativa
    # -----------------------------------------
    path("equipamentos/", listar_equipamentos, name="listar_equipamentos"),
    path("equipamentos/novo/", cadastrar_equipamento, name="cadastrar_equipamento"),
    path("equipamentos/editar/<int:id>/", editar_equipamento, name="editar_equipamento"),
    path("equipamentos/excluir/<int:id>/", excluir_equipamento, name="excluir_equipamento"),

    # -----------------------------------------
    # 📋 CONTROLE DE EPI
    # -----------------------------------------
    path("epi/controlar/", controlar_epi, name="controlar_epi"),

    # -----------------------------------------
    # 📊 RELATÓRIOS
    # -----------------------------------------
    path("relatorios/colaborador/", relatorio_colaborador, name="relatorio_colaborador"),
]
