# 🦺 Projeto EPI — Sistema de Gestão de Equipamentos de Proteção Individual

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Django](https://img.shields.io/badge/Django-5.x-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## 📖 Sobre o projeto

O **Projeto EPI** é uma aplicação web desenvolvida em **Django** que tem como objetivo **gerenciar o controle de EPIs (Equipamentos de Proteção Individual)** dentro de empresas e canteiros de obras.

O sistema permite cadastrar colaboradores, controlar empréstimos de EPIs, gerar relatórios de conformidade e manter o histórico de cada funcionário — tudo isso de forma simples, rápida e segura.

---

## 🚀 Funcionalidades principais

- 👷 **Cadastro de colaboradores** — com dados básicos como nome, e-mail e telefone  
- 🧤 **Controle de EPIs** — registre empréstimos, devoluções e validade dos equipamentos  
- 📋 **Relatórios automáticos** — exporte relatórios de controle e conformidade em PDF  
- 🔐 **Área administrativa** — login seguro para gestores  
- 🌐 **Área pública** — visitantes podem cadastrar contas e solicitar demonstrações  
- 💬 **Página de contato** — integração com WhatsApp e envio de mensagens  
- 💼 **Planos e serviços** — planos “Starter”, “Business” e “Enterprise” com opções de demonstração  

---

## 🧩 Tecnologias utilizadas

| Tecnologia | Descrição |
|-------------|------------|
| **Python 3.11** | Linguagem principal |
| **Django 5.x** | Framework backend |
| **Bootstrap 5** | Estilização e layout responsivo |
| **HTML / CSS / JS** | Frontend |
| **SQLite3** | Banco de dados padrão (modo local) |

---

## ⚙️ Como executar o projeto

### 🔧 Pré-requisitos
- Python 3.10+ instalado
- Git instalado
- Virtualenv (opcional, mas recomendado)

### 🧠 Passos para rodar localmente

```bash
# Clone o repositório
git clone https://github.com/Eisziel/ProjetoEPI.git

# Entre na pasta
cd ProjetoEPI

# Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate  # (Windows)

# Instale as dependências
pip install -r requirements.txt

# Rode as migrações
python manage.py migrate

# Inicie o servidor local
python manage.py runserver
