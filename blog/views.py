from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post

# 1. LISTAR (Read)
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

# 2. DETALHES (Read)
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# 3. CRIAR (Create)
class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['titulo', 'conteudo', 'autor'] # Incluímos 'autor' aqui

# 4. EDITAR (Update)
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['titulo', 'conteudo'] # Não deixamos mudar o autor na edição

# 5. DELETAR (Delete)
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('lista_posts')