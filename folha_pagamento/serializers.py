from rest_framework import serializers
from decimal import Decimal

class FolhaPagamentoSerializer(serializers.Serializer):
    
    salario_base = serializers.DecimalField(
        max_digits=10, ## permite salários de até 99 milhoes
        decimal_places=2, 
        min_value=Decimal('1518.00'), ## impede que o salário seja menor que o salário mínimo, usei decimal pra evitar erro no django
        error_messages={ ## personalizando a mensagem de erro
            'min_value': 'O salário não pode ser inferior ao mínimo (R$ 1.518,00).',
            'invalid': 'Informe um número válido.'
        }
    )
    horas_extras = serializers.DecimalField(
        max_digits=5,         # aceita ate 999.99 horas
        decimal_places=2,     # aceita quebrados
        min_value=Decimal('0.00'), 
        default=0,
        required=False
    )
    faltas = serializers.IntegerField( ## aceita apenas numeros inteiros (não pode 1.5 faltas)
        min_value=0, # impedindo valores negativos
        max_value=30, # regra de negocio: ngm pode faltar mais de 30 dias no mes
        default=0,
        required=False
    )
    nome = serializers.CharField(required=False) ## campo de identificação no rankin