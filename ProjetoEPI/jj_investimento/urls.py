from django.contrib import admin
from django.urls import path
from page_app.views import (
    index, contato, services, info,
    listar_colaboradores, criar_colaborador, editar_colaborador, excluir_colaborador,
    login_admin, logout_admin,
    cadastrar_colaborador, cadastrar_obrigado
)

urlpatterns = [
    # Admin padrão do Django
    path('admin/', admin.site.urls),

    # Páginas públicas
    path('', index, name='index'),
    path('contato/', contato, name='contato'),
    path('services/', services, name='services'),  # mantém a página antiga de serviços
    path('info/', info, name='info'),  # nova página de planos

    # Login / Logout
    path('login/', login_admin, name='login'),
    path('entrar/', login_admin, name='entrar'),
    path('logout/', logout_admin, name='logout'),

    # Cadastro público
    path('cadastrar/', cadastrar_colaborador, name='cadastrar_colaborador'),
    path('cadastrar/obrigado/', cadastrar_obrigado, name='cadastrar_obrigado'),

    # CRUD de colaboradores (área administrativa)
    path('colaboradores/', listar_colaboradores, name='listar_colaboradores'),
    path('colaboradores/novo/', criar_colaborador, name='criar_colaborador'),
    path('colaboradores/editar/<int:id>/', editar_colaborador, name='editar_colaborador'),
    path('colaboradores/excluir/<int:id>/', excluir_colaborador, name='excluir_colaborador'),
]
