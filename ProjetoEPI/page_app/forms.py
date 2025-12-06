# page_app/forms.py
from django import forms

from .models import Colaborador, Equipamento, ControleEPI, UsuarioSistema


class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'email', 'telefone', 'funcao', 'ativo']  # ✔ função adicionada
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'funcao': forms.Select(attrs={'class': 'form-select'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Colaborador.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Já existe um colaborador com esse e-mail.")
        return email


# 🔹 Formulário público (sem "ativo" e com senha ilustrativa)
class PublicColaboradorForm(forms.ModelForm):
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Campo ilustrativo — não usado para login real."
    )

    class Meta:
        model = Colaborador
        fields = ['nome', 'email', 'telefone', 'funcao']  # ✔ função adicionada
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'funcao': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Colaborador.objects.filter(email=email).exists():
            raise forms.ValidationError("Já existe um colaborador com esse e-mail.")
        return email


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'descricao', 'codigo', 'ca', 'quantidade_estoque']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'ca': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade_estoque': forms.NumberInput(attrs={'class': 'form-control'}),
        }


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
            'colaborador': forms.Select(attrs={'class': 'form-select'}),
            'equipamento': forms.Select(attrs={'class': 'form-select'}),
            'data_entrega': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'data_prevista_devolucao': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'data_devolucao': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'observacao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'observacao_devolucao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Status inicial limitado, como você definiu
        status_iniciais = ['EMPRESTADO', 'EM_USO', 'FORNECIDO']
        if not self.instance.pk:
            self.fields['status'].choices = [
                c for c in self.fields['status'].choices if c[0] in status_iniciais
            ]

class ControleEPIStatusForm(forms.ModelForm):
    """
    Formulário usado na EDIÇÃO da movimentação:
    - Permite alterar apenas status, data_devolucao e observacao_devolucao.
    - Colaborador, equipamento, datas de entrega/prevista ficam travados na tela.
    """
    class Meta:
        model = ControleEPI
        fields = ["status", "data_devolucao", "observacao_devolucao"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-select"}),
            "data_devolucao": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control",
            }),
            "observacao_devolucao": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
            }),
        }

class UsuarioSistemaForm(forms.ModelForm):
    confirmar_senha = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UsuarioSistema
        fields = ['nome', 'email', 'username', 'senha', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'senha': forms.PasswordInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned = super().clean()
        senha = cleaned.get("senha")
        confirmar = cleaned.get("confirmar_senha")

        if senha and confirmar and senha != confirmar:
            raise forms.ValidationError("As senhas não conferem.")

        return cleaned
