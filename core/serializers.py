from rest_framework import serializers
from .models import Funcionario, FolhaPagamento
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=['manager', 'employee'])
    salary = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está cadastrado.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class FuncionarioSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='nome')
    salary = serializers.DecimalField(source='salario_base', max_digits=10, decimal_places=2)
    role = serializers.SerializerMethodField()

    class Meta:
        model = Funcionario
        fields = ['id', 'name', 'email', 'salary', 'role', 'cargo']

    def get_role(self, obj):
        return 'employee'

class FolhaPagamentoSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='funcionario.id', read_only=True)
    month = serializers.CharField(source='mes_referencia')
    createdAt = serializers.DateTimeField(source='data_emissao', format="%Y-%m-%dT%H:%M:%SZ")
    
    baseSalary = serializers.DecimalField(source='funcionario.salario_base', max_digits=10, decimal_places=2, read_only=True)
    overtimeHours = serializers.DecimalField(source='qtd_horas_extras', max_digits=5, decimal_places=2)
    overtimeValue = serializers.DecimalField(source='valor_horas_extras', max_digits=10, decimal_places=2)
    bonuses = serializers.DecimalField(source='bonus', max_digits=10, decimal_places=2)
    deductions = serializers.DecimalField(source='deducoes_manuais', max_digits=10, decimal_places=2)
    
    grossSalary = serializers.DecimalField(source='salario_bruto', max_digits=10, decimal_places=2)
    netSalary = serializers.DecimalField(source='salario_liquido', max_digits=10, decimal_places=2)
    

    class Meta:
        model = FolhaPagamento
        fields = [
            'id', 'userId', 'month', 'createdAt', 'baseSalary',
            'overtimeHours', 'overtimeValue', 'bonuses', 'deductions',
            'grossSalary', 'inss', 'irrf', 'netSalary'
        ]

class CalculoInputSerializer(serializers.Serializer):
    employeeId = serializers.IntegerField()
    month = serializers.CharField()
    overtimeHours = serializers.DecimalField(max_digits=5, decimal_places=2, default=0)
    bonuses = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
