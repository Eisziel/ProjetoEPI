from django.urls import path
from page_app.views import (
    index, contato, services, entrar,
    login_admin, logout_admin,
    listar_colaboradores, criar_colaborador, editar_colaborador, excluir_colaborador,
    cadastrar_colaborador, cadastrar_obrigado  # 👈 Adicionados aqui
)

urlpatterns = [
    # ----------------------------
    # 🌐 Páginas principais (públicas)
    # ----------------------------
    path('', index, name='index'),
    path('contato/', contato, name='contato'),
    path('services/', services, name='services'),

    # ----------------------------
    # 🟢 Cadastro público de colaboradores
    # ----------------------------
    path('cadastrar/', cadastrar_colaborador, name='cadastrar_colaborador'),
    path('cadastrar/obrigado/', cadastrar_obrigado, name='cadastrar_obrigado'),

    # ----------------------------
    # 🔐 Login / Logout do Administrador
    # ----------------------------
    path('login/', login_admin, name='login'),
    path('logout/', logout_admin, name='logout'),

    # ----------------------------
    # 👨‍💼 CRUD de Colaboradores (somente ADM logado)
    # ----------------------------
    path('colaboradores/', listar_colaboradores, name='listar_colaboradores'),
    path('colaboradores/novo/', criar_colaborador, name='criar_colaborador'),
    path('colaboradores/editar/<int:id>/', editar_colaborador, name='editar_colaborador'),
    path('colaboradores/excluir/<int:id>/', excluir_colaborador, name='excluir_colaborador'),
]
