# Sistema de Folha de Pagamento - Backend Django

Este sistema permite que uma empresa gere folhas de pagamento mensais para funcionários.

## Tipos de Usuários

| Usuário | Permissões |
|---------|------------|
| Gerente | Cadastra funcionários, informa horas extras/faltas, gera a folha e o comprovante. |
| Funcionário | Apenas visualiza seu próprio comprovante. |

---

## Funcionalidades

- Login e autenticação
- Cadastro de funcionários
- Registro de horas extras e faltas
- Cálculo automático de salário líquido
- Geração de comprovante de folha

---

## Tecnologias Utilizadas

- Python (3.12+)
- Django
- Django REST Framework
- SQLite (desenvolvimento)

---

## Como Rodar o Projeto (Tutorial para Desenvolvedores)

### 1. Clonar o Repositório

```bash
git clone https://github.com/SEU_USUARIO/folha-pagamento.git
cd folha-pagamento
```

### 2. Criar o Ambiente Virtual (Obrigatório)

Cada desenvolvedor deve criar seu próprio ambiente virtual.

**Criar o ambiente virtual:**

```bash
python -m venv venv
```

**Ativar o ambiente virtual:**


```bash
venv\Scripts\activate
```




### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

**Caso o arquivo `requirements.txt` ainda não exista:**

```bash
pip install django djangorestframework
pip freeze > requirements.txt
```

### 4. Aplicar Migrations e Rodar o Servidor

```bash
python manage.py migrate
python manage.py runserver
```

**Servidor rodando em:** [http://localhost:8000/](http://localhost:8000/)

---

## Fluxo de Trabalho no Git (IMPORTANTE)

Cada desenvolvedor trabalha em uma branch própria.

### Criar uma Nova Branch

```bash
git checkout -b backend/nome-da-feature
```

### Exemplos de Branches

| Branch | Responsável | Conteúdo |
|--------|-------------|----------|
| backend/models | Dev 1 | Models, migrations, admin |
| backend/services | Dev 2 | Lógica de cálculo da folha |
| backend/auth | Dev 3 | Auth, permissões, roles |

### Enviar Alterações para o Repositório

```bash
git add .
git commit -m "feat: descrição do que foi feito"
git push origin backend/nome-da-feature
```

---



## Contribuindo

1. Crie sua branch de feature
2. Faça commit das suas alterações
3. Faça push para a branch
4. Abra um Pull Request, ele aparece assim que você conclui seu commit dentro do site do GitHub.

---

