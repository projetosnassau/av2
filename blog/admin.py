from django.contrib import admin
from .models import Post, Funcionario  # <--- Garanta que Funcionario está importado aqui

# Registra o Post
admin.site.register(Post)

# Registra o Funcionário (Essa é a linha que deve estar faltando)
admin.site.register(Funcionario)

