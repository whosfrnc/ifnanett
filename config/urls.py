from django.urls import path
from django.conf import settings
from django.contrib import admin
from app import views
from django.conf.urls.static import static
from app.views import (
    IndexView,
    LoginView,
    RegisterView,
    LogoutView,
    DeletePostView,
    perfil_view,
    edit_profile_view,
    SuporteView,
    PostarView,
    EditarUsuarioView,
    EditarPerfilUsuarioView,
    perfil,
    editar_perfil,
    deletar_comentario,
    deletar_conta,
    CustomPasswordResetView,
    suporte_view  
)

urlpatterns = [
    path('editar_perfil/', editar_perfil, name='editar_perfil'),
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),  # Página inicial
    path('login/', LoginView.as_view(), name='login'),  # Página de login
    path('register/', RegisterView.as_view(), name='register'),  # Página de registro
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout
    path('perfil/', perfil_view, name='perfil'),  # Página de perfil
    path('criar-postagem/', views.criar_postagem, name='criar_postagem'),
    path('editar_perfil/', edit_profile_view, name='editar_perfil'),  # Página para editar perfil
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_users/', views.admin_users, name='admin_users'),
    path('admin_support/', views.admin_support, name='admin_support'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('suporte/', suporte_view, name='suporte'),  # Mantenha apenas uma referência
    path('postar/', PostarView.as_view(), name='postar'),  # Página de postar
    path('deletar-conta/', deletar_conta, name='deletar_conta'),
    path('deletar/<int:id>/', DeletePostView.as_view(), name='deletar_post'),  # Certifique-se de que o nome do argumento é 'id'
    path('comentar/<int:postagem_id>/', views.comentar_postagem, name='comentar_postagem'),
    path('comentario/deletar/<int:comentario_id>/', deletar_comentario, name='deletar_comentario'),
    path('curtir/<int:postagem_id>/', views.curtir_postagem, name='curtir_postagem'),   
    path('editar_usuario/', EditarUsuarioView.as_view(), name='editar_usuario'),  # Editar usuário
    path('editar_perfil_usuario/', EditarPerfilUsuarioView.as_view(), name='editar_perfil_usuario'),  # Editar perfil do usuário
    path('agenda/', views.agenda, name='agenda'),  # Página da agenda
    path('adicionar_tarefa/', views.adicionar_tarefa, name='adicionar_tarefa'),  # URL para adicionar tarefa
    path('remover_tarefa/<int:id>/', views.remover_tarefa, name='remover_tarefa'),  # URL para remover tarefa
    path('perfil/<int:usuario_id>/', views.perfil_usuario, name='perfil_usuario'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
