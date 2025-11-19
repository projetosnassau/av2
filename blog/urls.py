from django.urls import path
# Importamos as classes que criamos no views.py
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView
)

urlpatterns = [
    # 1. A página inicial vai listar os posts (READ - Lista)
    path('', PostListView.as_view(), name='lista_posts'),

    # 2. Ver os detalhes de um post (READ - Detalhe)
    # <int:pk> pega o ID do post da URL
    path('post/<int:pk>/', PostDetailView.as_view(), name='detalhe_post'),

    # 3. Criar um novo post (CREATE)
    path('post/novo/', PostCreateView.as_view(), name='criar_post'),

    # 4. Editar um post existente (UPDATE)
    path('post/<int:pk>/editar/', PostUpdateView.as_view(), name='editar_post'),

    # 5. Deletar um post (DELETE)
    path('post/<int:pk>/deletar/', PostDeleteView.as_view(), name='deletar_post'),
]