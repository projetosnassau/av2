# Sistema de Folha de Pagamento - Módulo de Cálculos (Dev 2)

Este documento detalha as implementações realizadas na branch `backend/services`, responsável pela Camada de Serviços, Regras de Negócio e View de Processamento.

## Funcionalidades Implementadas

### 1. Regras de Negócio

Toda a lógica foi isolada no arquivo `services.py` para garantir segurança e facilidade de manutenção.

- **Cálculo de Valor Hora:** Baseado na carga horária padrão de **220 horas mensais**.
- **Horas Extras:** Cálculo automático com acréscimo de **50%** sobre o valor da hora normal.
- **Faltas:** Desconto proporcional calculado sobre o valor da diária (Salário / 30).
- **INSS (Atualizado 2025):** Implementação da tabela progressiva com as novas faixas e teto de desconto de **R$ 951,62**.
- **IRRF (Atualizado 2025/2026):** Cálculo sobre a base deduzida (Bruto - INSS) respeitando a nova faixa de isenção (**até R$ 2.428,80**).

### 2. API (Views)

Criação do endpoint que recebe os dados brutos e devolve o holerite calculado.

- **Validação de Dados:** O sistema bloqueia salários negativos ou zerados.
- **Tratamento de Erros:** Respostas HTTP padronizadas (400 Bad Request) para dados inválidos.
- **Formato JSON:** Comunicação padronizada para integração com o Front-end.

## Documentação da API

Como o Dev 3 ficará responsável pelas Rotas (`urls.py`), a View abaixo deve ser conectada ao endpoint sugerido `/api/calcular/`.

### Requisição (POST)

Enviar um JSON contendo os dados do funcionário para o mês corrente.

```
{
  "salario_base": 2500.00,
  "horas_extras": 0,
  "faltas": 0
}

```

### Resposta de Sucesso (200 OK)

O sistema retorna o cálculo detalhado pronto para exibição.

```
{
    "salario_bruto": 2500.0,
    "salario_liquido": 2297.77,
    "desconto_inss": 202.23,
    "desconto_irrf": 0.0
}

```

### Resposta de Erro (400 Bad Request)

Exemplo de retorno caso o salário base não seja enviado.

```
{
    "erro": "O salário base é obrigatório e deve ser positivo!"
}

```

## Tecnologias e Estrutura

- **`services.py`**: Classe `CalculadoraFolhaPagamento` (Lógica Pura).
- **`views.py`**: Classe `FolhaPagamentoView` (Interface API).
- **`tests.py`**: Testes Unitários automatizados.

## Como Rodar os Testes

Para garantir a integridade dos cálculos matemáticos (especialmente as faixas de impostos), foram criados testes unitários. Para executar a bateria de testes, rode no terminal:

```
python manage.py test folha_pagamento

```

**Cenários Cobertos:**

1.  Cálculo de salário padrão (R$ 2.500,00) conferindo INSS e IRRF.
2.  Validação de envio de dados vazios.
3.  Validação de valores negativos.
