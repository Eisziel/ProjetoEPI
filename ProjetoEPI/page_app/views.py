# page_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json

from .models import Colaborador, Equipamento, ControleEPI, UsuarioSistema
from .forms import (
    ColaboradorForm,
    PublicColaboradorForm,
    EquipamentoForm,
    ControleEPIForm,
    ControleEPIStatusForm,
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
# 🔹 CADASTRO PÚBLICO DE CONTAS
# =========================================================
def cadastrar_colaborador(request):
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
# 🔹 USUÁRIO DO SISTEMA (Login próprio)
# =========================================================
def cadastrar_usuario(request):
    if request.method == "POST":
        form = UsuarioSistemaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário do sistema cadastrado com sucesso!")
            return redirect("cadastrar_usuario")
        else:
            messages.error(request, "Falha ao cadastrar usuário. Verifique os campos.")
    else:
        form = UsuarioSistemaForm()

    return render(request, "page_app/usuarios/cadastrar.html", {
        "form": form,
        "titulo": "Cadastrar Usuário do Sistema",
    })


def entrar(request):
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
            messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "page_app/usuarios/login.html")


def logout_usuario(request):
    for key in ("usuario_id", "usuario_nome", "usuario_email"):
        request.session.pop(key, None)

    messages.info(request, "Você saiu do sistema.")
    return redirect("entrar")


# =========================================================
# 🔹 PERFIL / CONFIGURAÇÕES / AJUDA
# =========================================================
def perfil_usuario(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        messages.error(request, "Você precisa estar logado para acessar o perfil.")
        return redirect("entrar")

    usuario = get_object_or_404(UsuarioSistema, pk=usuario_id, ativo=True)
    return render(request, "page_app/usuarios/perfil.html", {"usuario": usuario})


def configuracoes_usuario(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        messages.error(request, "Faça login para acessar as configurações.")
        return redirect("entrar")

    usuario = get_object_or_404(UsuarioSistema, pk=usuario_id, ativo=True)
    return render(request, "page_app/usuarios/configuracoes.html", {"usuario": usuario})


def ajuda_usuario(request):
    return render(request, "page_app/usuarios/ajuda.html")


# =========================================================
# 🔐 LOGIN ADMINISTRATIVO REAL (Django Admin)
# =========================================================
def login_admin(request):
    """
    Login administrativo REAL usando o User padrão do Django.
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
    messages.info(request, "Você saiu do modo administrativo.")
    return redirect('login')


# =========================================================
# 🔹 CRUD DE COLABORADORES
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
    if request.method == "POST":
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Colaborador cadastrado com sucesso!")
            return redirect('criar_colaborador')
        else:
            messages.error(request, "Erro ao cadastrar colaborador.")
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
            return redirect("listar_colaboradores")
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
        return redirect("listar_colaboradores")

    return render(request, "page_app/colaboradores/confirmar_exclusao.html", {
        "colaborador": colaborador
    })


# =========================================================
# 🔹 CRUD DE EQUIPAMENTOS
# =========================================================
def cadastrar_equipamento(request):
    if request.method == "POST":
        form = EquipamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipamento cadastrado com sucesso!")
            return redirect("cadastrar_equipamento")
        else:
            messages.error(request, "Erro ao cadastrar equipamento.")
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
        "busca": busca
    })


def editar_equipamento(request, id):
    equipamento = get_object_or_404(Equipamento, id=id)

    if request.method == "POST":
        form = EquipamentoForm(request.POST, instance=equipamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Equipamento atualizado com sucesso!")
            return redirect("listar_equipamentos")
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

    if request.method == "POST":
        equipamento.delete()
        messages.success(request, "Equipamento excluído com sucesso!")
        return redirect("listar_equipamentos")

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
            messages.success(request, "Registro salvo com sucesso!")
            return redirect("controlar_epi")
        else:
            messages.error(request, "Erro ao registrar controle de EPI.")
    else:
        form = ControleEPIForm()

    # lista de movimentações para editar estado posteriormente
    movimentos = ControleEPI.objects.select_related("colaborador", "equipamento").order_by("-data_entrega")

    return render(request, "page_app/epi/controlar.html", {
        "form": form,
        "movimentos": movimentos,
    })


def editar_controle_epi(request, id):
    """
    Permite editar APENAS o status da movimentação de EPI
    + data/observação da devolução.
    Colaborador, equipamento e datas de entrega NÃO são alterados aqui.
    """
    mov = get_object_or_404(ControleEPI, id=id)

    if request.method == "POST":
        form = ControleEPIStatusForm(request.POST, instance=mov)
        if form.is_valid():
            form.save()
            messages.success(request, "Status do EPI atualizado com sucesso!")
            return redirect("controlar_epi")
        else:
            messages.error(request, "Erro ao atualizar status do EPI. Verifique os campos.")
    else:
        form = ControleEPIStatusForm(instance=mov)

    return render(request, "page_app/epi/editar.html", {
        "form": form,
        "mov": mov,
        "titulo": "Atualizar status do EPI",
    })


def excluir_controle_epi(request, id):
    """
    Exclui uma movimentação de EPI (registro de empréstimo/fornecimento).
    """
    mov = get_object_or_404(ControleEPI, id=id)

    if request.method == "POST":
        mov.delete()
        messages.success(request, "Movimentação de EPI excluída com sucesso!")
        return redirect("controlar_epi")

    return render(request, "page_app/epi/confirmar_exclusao.html", {
        "mov": mov
    })



# =========================================================
# 🔹 RELATÓRIO COMPLETO (com filtros AND + cards + donut + paginação)
# =========================================================
def relatorio_colaborador(request):
    nome = request.GET.get("nome", "").strip()
    equipamento = request.GET.get("equipamento", "").strip()
    status = request.GET.get("status", "").strip()

    movimentos = ControleEPI.objects.select_related("colaborador", "equipamento").all()

    # Filtros (AND)
    if nome:
        movimentos = movimentos.filter(colaborador__nome__icontains=nome)

    if equipamento:
        movimentos = movimentos.filter(equipamento__nome__icontains=equipamento)

    if status:
        movimentos = movimentos.filter(status=status)

    # Cards resumo
    total_registros = movimentos.count()
    total_emprestado = movimentos.filter(status="EMPRESTADO").count()
    total_em_uso = movimentos.filter(status="EM_USO").count()
    total_fornecido = movimentos.filter(status="FORNECIDO").count()
    total_devolvido = movimentos.filter(status="DEVOLVIDO").count()
    total_danificado = movimentos.filter(status="DANIFICADO").count()
    total_perdido = movimentos.filter(status="PERDIDO").count()

    # Dados do gráfico donut
    agg = movimentos.values("status").annotate(qtd=Count("id"))

    status_legenda = {
        "EMPRESTADO": "Emprestado",
        "EM_USO": "Em uso",
        "FORNECIDO": "Fornecido",
        "DEVOLVIDO": "Devolvido",
        "DANIFICADO": "Danificado",
        "PERDIDO": "Perdido",
    }

    chart_labels = [status_legenda.get(x["status"], x["status"]) for x in agg]
    chart_data = [x["qtd"] for x in agg]

    # Paginação
    paginator = Paginator(movimentos.order_by("-data_entrega"), 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "page_app/relatorios/colaborador.html", {
        "page_obj": page_obj,
        "movimentos": page_obj.object_list,

        # filtros
        "nome_busca": nome,
        "equipamento_busca": equipamento,
        "status_busca": status,

        # cards
        "total_registros": total_registros,
        "total_emprestado": total_emprestado,
        "total_em_uso": total_em_uso,
        "total_fornecido": total_fornecido,
        "total_devolvido": total_devolvido,
        "total_danificado": total_danificado,
        "total_perdido": total_perdido,

        # gráfico
        "chart_labels_json": json.dumps(chart_labels),
        "chart_data_json": json.dumps(chart_data),

        # select de status
        "status_choices": ControleEPI.STATUS_CHOICES,
    })
