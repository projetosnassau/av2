# Sistema de Folha de Pagamento - Módulo de Cálculos e Análise (Dev 2)

Este documento detalha as implementações realizadas na branch `backend/services`. O módulo agora conta com validação de dados (Serializers) e serviços de análise gerencial.

## Funcionalidades Implementadas

### 1. Segurança e Validação (`serializers.py`)

Atendendo à solicitação de segurança, implementamos uma camada de validação que sanitiza os dados antes do processamento.

- **Tipagem Forte:** Conversão automática para `Decimal` (evita erros de arredondamento).
- **Travas de Negócio:**

  - Salário não pode ser inferior ao mínimo (R$ 1.518,00).
  - Bloqueio de números negativos.
  - Limite de 30 faltas por mês.

### 2. Análise Salarial (`services.py`)

Novo serviço capaz de processar lotes de funcionários.

- **Filtragem e Ranking:** Ordena a lista de pagamentos do maior para o menor salário líquido.
- **Estatísticas:** Calcula automaticamente:

  - Maior e Menor salário.
  - Média salarial da equipe.
  - Custo total da folha.

### 3. Regras de Cálculo (2025)

- **INSS:** Tabela progressiva 2025 (Teto R$ 951,62).
- **IRRF:** Tabela progressiva (Isenção até R$ 2.428,80).
- **Extras:** Adicional de 50%.
- **Faltas:** Desconto proporcional (Salário / 30).

## Documentação da API

O Dev 3 deve configurar as rotas no `urls.py` apontando para as Views criadas.

### Rota 1: Cálculo Individual

**Sugestão de URL:** `/api/calcular/` **Método:** `POST`

**Entrada (JSON):**

```
{
  "salario_base": 2500.00,
  "horas_extras": 0,
  "faltas": 0
}

```

**Saída de Sucesso (200 OK):**

```
{
    "salario_bruto": 2500.0,
    "salario_liquido": 2297.77,
    "desconto_inss": 202.23,
    "desconto_irrf": 0.0
}

```

### Rota 2: Análise de Lista (Gerencial)

**Sugestão de URL:** `/api/analisar/` **Método:** `POST` **Descrição:** Envie uma lista (array) de funcionários para gerar ranking e estatísticas.

**Entrada (JSON Array):**

```
[
  { "nome": "Gerente", "salario_base": 5000.00 },
  { "nome": "Assistente", "salario_base": 2000.00 },
  { "nome": "Estagiário", "salario_base": 1500.00 }
]

```

**Saída (JSON - Exemplo):**

```
{
    "relatorio_gerencial": {
        "total_funcionarios": 3,
        "maior_salario_liquido": 4118.57,
        "media_salarial": 2496.20,
        "folha_total_custo": 7488.60
    },
    "ranking_detalhado": [
        { "nome": "Gerente", "salario_liquido": 4118.57, ... },
        { "nome": "Assistente", "salario_liquido": 1820.03, ... },
        { "nome": "Estagiário", "salario_liquido": 1550.00, ... }
    ]
}

```

## Tecnologias e Estrutura

- **`serializers.py`**: Classe `FolhaPagamentoSerializer` (Validação e Segurança).
- **`services.py`**: Classes `CalculadoraFolhaPagamento` e `AnaliseSalarialService` (Lógica).
- **`views.py`**: Classes `FolhaPagamentoView` e `AnaliseSalarialView` (API).
- **`tests.py`**: Testes Unitários automatizados.

## Como Rodar os Testes

Para garantir a integridade dos cálculos matemáticos e das validações de segurança:

```
python manage.py test folha_pagamento

```

**Cenários Cobertos:**

1.  Cálculo de salário padrão (R$ 2.500,00) conferindo INSS e IRRF 2025.
2.  Validação de segurança (bloqueio de salário negativo e abaixo do mínimo).
3.  Ranking salarial (ordenação correta da lista e cálculo de estatísticas).
