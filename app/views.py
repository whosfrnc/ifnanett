from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser  # Certifique-se de que está importando seu modelo CustomUser
from .forms import EditProfileForm, EditPerfilUsuarioForm  # Importando os formulários
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm 
from .forms import UserUpdateForm 
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required
from .models import Suporte
from django.contrib.auth.decorators import login_required
from .models import Postagem
from .forms import PostagemForm
from django.shortcuts import get_object_or_404, redirect
from .models import Comentario
from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm
from django.contrib.auth.decorators import user_passes_test

class IndexView(View):
    def get(self, request):
        desenhos = Postagem.objects.all().order_by('-data_publicacao')  # Use 'data_publicacao' em vez de 'data_postagem'
        return render(request, 'index.html', {'postagens': desenhos})  # Altere para 'postagens' para corresponder ao seu template

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                user = None
            
            if user:
                user = authenticate(request, username=user.email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')  # Redireciona para a página principal
                else:
                    messages.error(request, 'Senha incorreta.')
            else:
                messages.error(request, 'Email não encontrado.')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
    
        return render(request, 'login.html')

@login_required
def perfil(request):
    user = request.user  # Obtém o usuário atual
    return render(request, 'perfil.html', {'user': user})

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email já existe'})
        
        user = CustomUser.objects.create_user(email=email, password=password)
        user.save()
        login(request, user)  # Faz login automaticamente após o registro
        return redirect('index')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')  # Redireciona para a página de login após logout


@login_required
def perfil_view(request):
    usuario = request.user  # ou obtenha o usuário de outra maneira
    return render(request, 'perfil.html', {'user': usuario})
def editar_perfil(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirecionar para a página de perfil após salvar
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'editar_perfil.html', {'form': form})
@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')  # Certifique-se de que a URL 'perfil' está correta
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'editar_perfil.html', {'form': form})

class SuporteView(View):
    def get(self, request):
        return render(request, 'suporte.html')

    def post(self, request):
        # Lógica para enviar suporte
        pass


class PostarView(View):
    def get(self, request):
        return render(request, 'postar.html')

    def post(self, request):
        # Lógica para postar
        pass




class EditarUsuarioView(View):
    @login_required
    def get(self, request):
        user = request.user.usuario
        form = EditUsuarioForm(instance=user)
        return render(request, 'editar_usuario.html', {'form': form})

    @login_required
    def post(self, request):
        user = request.user.usuario
        form = EditUsuarioForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('perfil')
        return render(request, 'editar_usuario.html', {'form': form})


class EditarPerfilUsuarioView(View):
    @login_required
    def get(self, request):
        perfil = request.user.perfilusuario
        form = EditPerfilUsuarioForm(instance=perfil)
        return render(request, 'editar_perfil_usuario.html', {'form': form})

    @login_required
    def post(self, request):
        perfil = request.user.perfilusuario
        form = EditPerfilUsuarioForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil de usuário atualizado com sucesso!')
            return redirect('perfil')
        return render(request, 'editar_perfil_usuario.html', {'form': form})


@login_required
def suporte_view(request):
    print("Requisição recebida: ", request.method)  # Adicione este print
    if request.method == "POST":
        usuario = request.user
        assunto = request.POST.get('assunto')
        mensagem = request.POST.get('mensagem')
        status = 'Em aberto'  # Definindo um status padrão para a mensagem de suporte

        # Salva o suporte no banco de dados
        Suporte.objects.create(usuario=usuario, assunto=assunto, mensagem=mensagem, status=status)

        # Mensagem de sucesso
        messages.success(request, 'Sua mensagem foi enviada com sucesso!')
        
        # Redireciona para a página de suporte ou para onde você quiser
        return redirect('suporte')  

    print("Renderizando o template suporte.html")  # Adicione este print
    return render(request, 'suporte.html')   

class PostarView(View):
    def get(self, request):
        return render(request, 'postar.html')  # Página para criar postagens

    def post(self, request):
        if request.method == 'POST':
            titulo = request.POST.get('titulo')
            imagem = request.FILES.get('imagem')  # Obtém a imagem do formulário
            usuario = request.user  # Usuário atual

            # Cria uma nova postagem
            Postagem.objects.create(titulo=titulo, imagem=imagem, usuario=usuario)
            return redirect('index')  # Redireciona para a página principal após criar a postagem

@login_required
def criar_postagem(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        imagem = request.FILES.get('imagem')  # Obtém a imagem do formulário
        usuario = request.user  # Usuário atual

        # Verifica se o título não está vazio
        if titulo:
            # Cria uma nova postagem
            Postagem.objects.create(titulo=titulo, imagem=imagem, usuario=usuario)
            messages.success(request, "Postagem criada com sucesso!")  # Mensagem de sucesso
            return redirect('index')  # Redireciona para a página principal após criar a postagem
        else:
            messages.error(request, "O título é obrigatório.")  # Mensagem de erro se o título estiver vazio

    return render(request, 'criar_postagem.html')  # Rend
class DeletePostView(View):
    def post(self, request, id):
        # Usando get_object_or_404 para lidar com o caso de o objeto não existir
        postagem = get_object_or_404(Postagem, id=id)
        postagem.delete()
        return redirect('index')  # Redireciona para a página inicia
    
    
@login_required
def comentar_postagem(request, postagem_id):
    postagem = Postagem.objects.get(id=postagem_id)
    if request.method == 'POST':
        conteudo = request.POST['conteudo']
        comentario = Comentario(postagem=postagem, usuario=request.user, conteudo=conteudo)
        comentario.save()
    return redirect('index')

def curtir_postagem(request, postagem_id):
    postagem = get_object_or_404(Postagem, id=postagem_id)
    
    # Verifica se o usuário já curtiu a postagem
    if request.user in postagem.curtidas.all():
        postagem.curtidas.remove(request.user)  # Remove a curtida se o usuário já tiver curtido
    else:
        postagem.curtidas.add(request.user)  # Adiciona a curtida se o usuário não tiver curtido ainda

    return redirect('index')  # Redireciona de volta para o index (ou outra página que deseje)


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'seu_template/password_reset.html'  # Ajuste o caminho do template
    email_template_name = 'seu_template/password_reset_email.html'  # Ajuste o caminho do email
    subject_template_name = 'seu_template/password_reset_subject.txt'  # Ajuste o caminho do assunto
    success_url = 'password_reset_done/'  # Ajuste a URL conforme necessário
    
def is_admin(user):
    return user.is_staff

# Dashboard administrativo
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Listagem de usuários
@user_passes_test(is_admin)
def admin_users(request):
    usuarios = CustomUser.objects.all()
    return render(request, 'admin_users.html', {'usuarios': usuarios})

# Listagem de mensagens de suporte
@user_passes_test(is_admin)
def admin_support(request):
    mensagens = Suporte.objects.all()  # Busca todas as mensagens de suporte
    return render(request, 'admin_support.html', {'mensagens': mensagens})
# Apagar usuário
@user_passes_test(is_admin)
def delete_user(request, user_id):
    usuario = get_object_or_404(CustomUser, id=user_id)
    usuario.delete()
    return redirect('admin_users')

def inicio_view(request):
    return render(request, 'inicio.html')  # Renderiza a página início.html

@login_required
def deletar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    # Verifica se o usuário é o dono do comentário ou administrador
    if request.user == comentario.usuario or request.user.is_superuser:
        comentario.delete()
        messages.success(request, 'Comentário apagado com sucesso!')
    else:
        messages.error(request, 'Você não tem permissão para apagar este comentário.')

    return redirect('index')  # Altere para a página correta de redirecionamento

@login_required
def deletar_conta(request):
    if request.method == 'POST':
        # Apagar a conta do usuário
        request.user.delete()
        messages.success(request, "Conta apagada com sucesso.")
        return redirect('início')  # Redireciona para a página i
