from django.db import models
from django.contrib.auth.models import User

class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='funcionario_profile')
    
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cargo = models.CharField(max_length=50, default="Funcionário")
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    data_admissao = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome

class FolhaPagamento(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    mes_referencia = models.CharField(max_length=7)
    
    qtd_horas_extras = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deducoes_manuais = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    qtd_faltas = models.IntegerField(default=0)

    valor_horas_extras = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_faltas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    salario_bruto = models.DecimalField(max_digits=10, decimal_places=2)
    inss = models.DecimalField(max_digits=10, decimal_places=2)
    irrf = models.DecimalField(max_digits=10, decimal_places=2)
    salario_liquido = models.DecimalField(max_digits=10, decimal_places=2)
    
    data_emissao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.funcionario.nome} - {self.mes_referencia}"