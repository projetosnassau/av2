from django.db import models
from django.urls import reverse 

# 1. Modelo Funcionario (o Autor)
class Funcionario(models.Model):
    Nome = models.CharField(max_length=100)
    CPF = models.CharField(max_length=14, unique=True)
    Email = models.EmailField(unique=True)
    Telefone = models.CharField(max_length=15)
    Data_de_nascimento = models.DateField()
    RG = models.CharField(max_length=12, unique=True)
    Endereco = models.CharField(max_length=200)
    Bairro = models.CharField(max_length=100)

    def __str__(self):
        return self.Nome

# 2. Modelo Post (a Publicação)
class Post(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    # Relação: Um Post tem um autor (Funcionario)
    autor = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    # Redirecionamento após criar/editar
    def get_absolute_url(self):
        return reverse('detalhe_post', args=[str(self.id)])
    

    