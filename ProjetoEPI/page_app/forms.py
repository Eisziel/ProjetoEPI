# page_app/forms.py
from django import forms

from .models import Colaborador, Equipamento, ControleEPI, UsuarioSistema


class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'email', 'telefone', 'ativo']  # ✔ arrumado

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Colaborador.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Já existe um colaborador com esse e-mail.")
        return email


# 🔹 Formulário público (usado em cadastrar_colaborador)
class PublicColaboradorForm(forms.ModelForm):
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
        required=False,
        help_text="Campo ilustrativo, não usado para login real."
    )

    class Meta:
        model = Colaborador
        fields = ['nome', 'email', 'telefone']  # senha é extra, não vai no model

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Colaborador.objects.filter(email=email).exists():
            raise forms.ValidationError("Já existe um colaborador com esse e-mail.")
        return email


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'descricao', 'codigo', 'ca', 'quantidade_estoque']


class ControleEPIForm(forms.ModelForm):
    class Meta:
        model = ControleEPI
        fields = [
            'colaborador',
            'equipamento',
            'data_entrega',
            'data_prevista_devolucao',
            'data_devolucao',
            'status',
            'observacao',
            'observacao_devolucao',
        ]
        widgets = {
            'data_entrega': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_prevista_devolucao': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_devolucao': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'observacao': forms.Textarea(attrs={'rows': 3}),
            'observacao_devolucao': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        status_iniciais = ['EMPRESTADO', 'EM_USO', 'FORNECIDO']
        if not self.instance.pk:
            self.fields['status'].choices = [
                c for c in self.fields['status'].choices if c[0] in status_iniciais
            ]


# 🔹 Formulário para Usuário do Sistema (login estático)
class UsuarioSistemaForm(forms.ModelForm):
    confirmar_senha = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput
    )

    class Meta:
        model = UsuarioSistema
        fields = ['nome', 'email', 'username', 'senha', 'ativo']
        widgets = {
            'senha': forms.PasswordInput,
        }

    def clean(self):
        cleaned = super().clean()
        senha = cleaned.get("senha")
        confirmar = cleaned.get("confirmar_senha")

        if senha and confirmar and senha != confirmar:
            raise forms.ValidationError("As senhas não conferem.")

        return cleaned
