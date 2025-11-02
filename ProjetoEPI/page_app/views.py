# page_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Colaborador
# Certifique-se de que PublicColaboradorForm exista em page_app/forms.py
from .forms import ColaboradorForm, PublicColaboradorForm


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
# 🔹 PÁGINAS PÚBLICAS
# =========================================================
def index(request):
    return render(request, "page_app/partial/home.html")


def contato(request):
    """
    Template de contato — pode aceitar query strings:
    ?plano=Business&acao=demo  -> você pode pré-preencher campos no template se quiser.
    """
    return render(request, "page_app/partial/contato.html")


def services(request):
    """
    Página principal de Services (mostra os planos).
    Envia 'planos' para o template services.html
    """
    return render(request, "page_app/partial/services.html", {"planos": PLANS})


def info(request):
    """
    Página de info/planos (manter para compatibilidade).
    Reutiliza os mesmos planos.
    """
    return render(request, "page_app/partial/info.html", {"planos": PLANS})


def welcome(request):
    return render(request, "page_app/partial/welcome.html")


def header(request):
    return render(request, "page_app/partial/header.html")


def footer(request):
    return render(request, "page_app/partial/footer.html")


# =========================================================
# 🔹 CADASTRO PÚBLICO DE CONTAS (sem login)
# =========================================================
def cadastrar_colaborador(request):
    """
    Formulário público mínimo: nome, email, telefone, senha.
    Usa PublicColaboradorForm (crie-o em page_app/forms.py).
    """
    if request.method == "POST":
        form = PublicColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('cadastrar_obrigado')
    else:
        form = PublicColaboradorForm()

    return render(request, "page_app/colaboradores/public_form.html", {
        "form": form,
        "titulo": "Cadastrar conta"
    })


def cadastrar_obrigado(request):
    return render(request, "page_app/colaboradores/obrigado.html")


# =========================================================
# 🔹 LOGIN / LOGOUT (Admin)
# =========================================================
def login_admin(request):
    """
    Login padrão (usado em /login/ e, se desejar, /entrar/).
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect('listar_colaboradores')
        else:
            messages.error(request, "Usuário ou senha incorretos.")
    return render(request, "page_app/admin/login.html")


@login_required
def logout_admin(request):
    logout(request)
    return redirect('login')


# =========================================================
# 🔹 CRUD DE COLABORADORES (Área ADM)
# =========================================================
@login_required
def listar_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    return render(request, "page_app/colaboradores/listar.html", {
        "colaboradores": colaboradores
    })


@login_required
def criar_colaborador(request):
    if request.method == "POST":
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Colaborador cadastrado com sucesso!")
            return redirect('listar_colaboradores')
    else:
        form = ColaboradorForm()
    return render(request, "page_app/colaboradores/form.html", {
        "form": form,
        "titulo": "Novo Colaborador"
    })


@login_required
def editar_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    if request.method == "POST":
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            messages.success(request, "Colaborador atualizado com sucesso!")
            return redirect('listar_colaboradores')
    else:
        form = ColaboradorForm(instance=colaborador)
    return render(request, "page_app/colaboradores/form.html", {
        "form": form,
        "titulo": "Editar Colaborador"
    })


@login_required
def excluir_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    colaborador.delete()
    messages.success(request, "Colaborador removido com sucesso!")
    return redirect('listar_colaboradores')


# =========================================================
# 🔹 VIEW PÚBLICA "ENTRAR" (form público de login)
# =========================================================
def entrar(request):
    """
    Template público que apresenta o formulário de login para visitantes.
    Dentro dele incluir link para 'cadastrar_colaborador' (Cadastre-se aqui).
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect('listar_colaboradores')
        else:
            messages.error(request, "Usuário ou senha incorretos.")
    return render(request, "page_app/public/entrar.html")
