# page_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Colaborador, Equipamento, ControleEPI, UsuarioSistema
from .forms import (
    ColaboradorForm,
    PublicColaboradorForm,
    EquipamentoForm,
    ControleEPIForm,
    UsuarioSistemaForm,
)

# =========================================================
# Dados de planos (fonte única para services e info)
# =========================================================
PLANS = [
    {
        "nome": "Starter",
        "preco": "Gratuito",
        "desc": "Ideal para pequenas equipes testarem o sistema.",
        "features": [
            "Até 10 colaboradores",
            "Cadastro básico de EPIs",
            "Relatórios simples"
        ],
        "impact": [
            "Redução de falhas operacionais",
            "Implementação em minutos",
        ],
        "popular": False,
    },
    {
        "nome": "Business",
        "preco": "R$ 99/mês",
        "desc": "Para empresas que precisam de mais controle e automação.",
        "features": [
            "Colaboradores ilimitados",
            "Controle completo de EPIs",
            "Exportar relatórios em PDF",
            "Acesso multiusuário"
        ],
        "impact": [
            "Redução em até 30% no tempo de gestão de EPIs",
            "Relatórios automáticos para auditoria",
        ],
        "popular": True,
    },
    {
        "nome": "Enterprise",
        "preco": "Sob consulta",
        "desc": "Solução personalizada para grandes organizações.",
        "features": [
            "Treinamento e suporte dedicado",
            "Integração com estoque / RH",
            "Customização de relatórios",
            "Suporte prioritário"
        ],
        "impact": [
            "Solução totalmente integrada ao RH/ERP",
            "SLA de atendimento prioritário",
        ],
        "popular": False,
    },
]


# =========================================================
# 🔹 PÁGINAS PÚBLICAS / LANDING
# =========================================================
def index(request):
    return render(request, "page_app/partial/home.html")


def contato(request):
    return render(request, "page_app/partial/contato.html")


def services(request):
    return render(request, "page_app/partial/services.html", {"planos": PLANS})


def info(request):
    return render(request, "page_app/partial/info.html", {"planos": PLANS})


def welcome(request):
    return render(request, "page_app/partial/welcome.html")


def header(request):
    return render(request, "page_app/partial/header.html")


def footer(request):
    return render(request, "page_app/partial/footer.html")


# =========================================================
# 🔹 CADASTRO PÚBLICO DE CONTAS (sem login real de sistema)
# =========================================================
def cadastrar_colaborador(request):
    """
    Formulário público mínimo: nome, email, telefone, senha (ilustrativa).
    Usa PublicColaboradorForm.
    """
    if request.method == "POST":
        form = PublicColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('cadastrar_obrigado')
        else:
            messages.error(request, "Erro ao realizar cadastro. Verifique os dados.")
    else:
        form = PublicColaboradorForm()

    return render(request, "page_app/colaboradores/public_form.html", {
        "form": form,
        "titulo": "Cadastrar conta"
    })


def cadastrar_obrigado(request):
    return render(request, "page_app/colaboradores/obrigado.html")


# =========================================================
# 🔹 USUÁRIO DO SISTEMA (para exibir nome/foto, login estático)
# =========================================================
def cadastrar_usuario(request):
    """
    Cadastro de usuários do sistema (técnico, responsável etc.).
    - exibe mensagem de sucesso/falha
    - permanece na tela de cadastro
    - usa UsuarioSistemaForm (com confirmação de senha)
    """
    if request.method == "POST":
        form = UsuarioSistemaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário do sistema cadastrado com sucesso!")
            form = UsuarioSistemaForm()  # limpa o formulário
        else:
            messages.error(request, "Falha ao cadastrar usuário. Verifique os campos.")
    else:
        form = UsuarioSistemaForm()

    return render(request, "page_app/usuarios/cadastrar.html", {
        "form": form,
        "titulo": "Cadastrar Usuário do Sistema",
    })


def entrar(request):
    """
    Login simples baseado em UsuarioSistema (sessão própria).
    """
    if request.method == "POST":
        username = request.POST.get("username")
        senha = request.POST.get("senha")

        try:
            usuario = UsuarioSistema.objects.get(username=username, senha=senha, ativo=True)
        except UsuarioSistema.DoesNotExist:
            usuario = None

        if usuario:
            request.session["usuario_id"] = usuario.id
            request.session["usuario_nome"] = usuario.nome
            request.session["usuario_email"] = usuario.email
            messages.success(request, "Login realizado com sucesso!")
            return redirect("index")
        else:
            messages.error(request, "Usuário ou senha inválidos, ou usuário inativo.")

    return render(request, "page_app/usuarios/login.html")


def logout_usuario(request):
    """
    Logout simples: limpa os dados do usuário da sessão.
    """
    for key in ("usuario_id", "usuario_nome", "usuario_email"):
        request.session.pop(key, None)

    messages.info(request, "Você saiu do sistema.")
    return redirect("entrar")


# ====== 🔹 MEU PERFIL / CONFIGURAÇÕES / AJUDA ==================
def perfil_usuario(request):
    """
    Mostra os dados do usuário logado (UsuarioSistema) usando a sessão.
    """
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        messages.error(request, "Você precisa estar logado para acessar o perfil.")
        return redirect("entrar")

    usuario = get_object_or_404(UsuarioSistema, pk=usuario_id, ativo=True)

    return render(request, "page_app/usuarios/perfil.html", {
        "usuario": usuario,
    })


def configuracoes_usuario(request):
    """
    Tela de configurações do usuário.
    """
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        messages.error(request, "Você precisa estar logado para acessar as configurações.")
        return redirect("entrar")

    usuario = get_object_or_404(UsuarioSistema, pk=usuario_id, ativo=True)

    return render(request, "page_app/usuarios/configuracoes.html", {
        "usuario": usuario,
    })


def ajuda_usuario(request):
    """
    Tela simples de ajuda ao usuário.
    """
    return render(request, "page_app/usuarios/ajuda.html")


# =========================================================
# 🔹 LOGIN / LOGOUT (Admin Django) – opcional
# =========================================================
def login_admin(request):
    """
    Login padrão do Django (área administrativa real).
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login administrativo realizado com sucesso!")
            return redirect('listar_colaboradores')
        else:
            messages.error(request, "Usuário ou senha administrativos incorretos.")
    return render(request, "page_app/admin/login.html")


def logout_admin(request):
    logout(request)
    return redirect('login')


# =========================================================
# 🔹 CRUD DE COLABORADORES (Área ADM)
# =========================================================
def listar_colaboradores(request):
    busca = request.GET.get("busca", "")
    colaboradores = Colaborador.objects.all()
    if busca:
        colaboradores = colaboradores.filter(
            Q(nome__icontains=busca) | Q(email__icontains=busca)
        )

    return render(request, "page_app/colaboradores/listar.html", {
        "colaboradores": colaboradores,
        "busca": busca,
    })



def criar_colaborador(request):
    """
    Atende aos requisitos:
    - cadastra colaborador
    - mostra mensagem de sucesso/falha
    - permanece na tela de cadastro após salvar
    """
    if request.method == "POST":
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Colaborador cadastrado com sucesso!")
            return redirect('criar_colaborador')
        else:
            messages.error(request, "Erro ao cadastrar colaborador. Verifique os campos.")
    else:
        form = ColaboradorForm()
    return render(request, "page_app/colaboradores/form.html", {
        "form": form,
        "titulo": "Cadastro de Colaboradores"
    })


def editar_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    if request.method == "POST":
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            messages.success(request, "Colaborador atualizado com sucesso!")
            return redirect('listar_colaboradores')
        else:
            messages.error(request, "Erro ao atualizar colaborador.")
    else:
        form = ColaboradorForm(instance=colaborador)
    return render(request, "page_app/colaboradores/form.html", {
        "form": form,
        "titulo": f"Editar Colaborador - {colaborador.nome}"
    })


def excluir_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)

    if request.method == "POST":
        colaborador.delete()
        messages.success(request, "Colaborador removido com sucesso!")
        return redirect('listar_colaboradores')

    return render(request, "page_app/colaboradores/confirmar_exclusao.html", {
        "colaborador": colaborador
    })


# =========================================================
# 🔹 EQUIPAMENTOS – Cadastro, listar, editar, excluir
# =========================================================
def cadastrar_equipamento(request):
    if request.method == "POST":
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipamento cadastrado com sucesso!")
            return redirect('cadastrar_equipamento')
        else:
            messages.error(request, "Erro ao cadastrar equipamento. Verifique os campos.")
    else:
        form = EquipamentoForm()
    return render(request, "page_app/equipamentos/form.html", {
        "form": form,
        "titulo": "Cadastro de Equipamentos"
    })


def listar_equipamentos(request):
    busca = request.GET.get("busca", "")
    equipamentos = Equipamento.objects.all()
    if busca:
        equipamentos = equipamentos.filter(
            Q(nome__icontains=busca) | Q(codigo__icontains=busca)
        )

    return render(request, "page_app/equipamentos/listar.html", {
        "equipamentos": equipamentos,
        "busca": busca,
    })


def editar_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)
    if request.method == "POST":
        form = EquipamentoForm(request.POST, instance=equipamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipamento atualizado com sucesso!")
            return redirect('listar_equipamentos')
        else:
            messages.error(request, "Erro ao atualizar equipamento.")
    else:
        form = EquipamentoForm(instance=equipamento)

    return render(request, "page_app/equipamentos/form.html", {
        "form": form,
        "titulo": f"Editar Equipamento - {equipamento.nome}"
    })


def excluir_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)

    # 🔹 corrigido: era "POST__"
    if request.method == "POST":
        equipamento.delete()
        messages.success(request, "Equipamento excluído com sucesso!")
        return redirect('listar_equipamentos')

    return render(request, "page_app/equipamentos/confirmar_exclusao.html", {
        "equipamento": equipamento
    })


# =========================================================
# 🔹 CONTROLE DE EPI
# =========================================================
def controlar_epi(request):
    if request.method == "POST":
        form = ControleEPIForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro de controle de EPI salvo com sucesso!")
            return redirect('controlar_epi')
        else:
            messages.error(request, "Erro ao salvar controle de EPI. Verifique os campos.")
    else:
        form = ControleEPIForm()

    return render(request, "page_app/epi/controlar.html", {
        "form": form
    })


# =========================================================
# 🔹 RELATÓRIO – EPIs por colaborador
# =========================================================
def relatorio_colaborador(request):
    nome = request.GET.get("nome", "")
    movimentos = ControleEPI.objects.select_related("colaborador", "equipamento")

    if nome:
        movimentos = movimentos.filter(colaborador__nome__icontains=nome)

    return render(request, "page_app/relatorios/colaborador.html", {
        "movimentos": movimentos,
        "nome_busca": nome,
    })
