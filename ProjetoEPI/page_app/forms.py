# page_app/forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Colaborador


class ColaboradorForm(forms.ModelForm):
    """Form interno (ADM) — usa todos os campos do modelo Colaborador."""
    class Meta:
        model = Colaborador
        fields = "__all__"


class PublicColaboradorForm(forms.Form):
    """
    Form público para 'Cadastrar conta' com os campos mínimos:
    nome, email, telefone, senha.

    O .save() cria um User (username=email) e tenta criar um Colaborador
    preenchendo automaticamente campos com nomes comuns.
    """
    nome = forms.CharField(label="Nome", max_length=150)
    email = forms.EmailField(label="E-mail")
    telefone = forms.CharField(label="Telefone", max_length=30, required=False)
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput, min_length=6)

    def clean_email(self):
        email = self.cleaned_data["email"]
        # opcional: garante unicidade do user/email
        if User.objects.filter(email=email).exists():
            raise ValidationError("Já existe uma conta com esse e-mail.")
        return email

    def save(self, commit=True):
        """
        Cria um User e tenta criar um Colaborador.
        Retorna a instância do Colaborador se conseguir, ou o User criado caso não exista Colaborador.
        """
        nome = self.cleaned_data.get("nome")
        email = self.cleaned_data.get("email")
        telefone = self.cleaned_data.get("telefone")
        senha = self.cleaned_data.get("senha")

        # 1) criar User (username = email)
        username = email
        user = User.objects.create_user(username=username, email=email, password=senha, first_name=nome)

        # 2) tentar criar Colaborador preenchendo campos conforme existam no Modelo
        try:
            model_fields = {f.name for f in Colaborador._meta.get_fields() if hasattr(f, "name")}
            # mapa de possíveis nomes de campo para cada dado
            mapping = {
                "nome": ["nome", "name", "full_name", "first_name"],
                "email": ["email", "e_mail", "mail"],
                "telefone": ["telefone", "phone", "phone_number", "telefone_celular"]
            }
            kwargs = {}

            # atribui user se existir campo relacionamento 'user' ou 'usuario'
            if "user" in model_fields:
                kwargs["user"] = user
            elif "usuario" in model_fields:
                kwargs["usuario"] = user

            # mapear nome, email, telefone para campos existentes do modelo
            for key, possibilities in mapping.items():
                for p in possibilities:
                    if p in model_fields:
                        kwargs[p] = {"nome": nome, "email": email, "telefone": telefone}[key]
                        break

            # Se o modelo exigir outros campos (ex.: obrigatório), isso pode lançar erro
            colaborador = Colaborador.objects.create(**kwargs)
            return colaborador
        except Exception:
            # fallback — se não conseguir criar o Colaborador, apenas devolve o User criado
            # para não perder o cadastro. Você pode logar esse erro para debug.
            return user
