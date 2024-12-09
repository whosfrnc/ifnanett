from django import forms
from .models import CustomUser, PerfilUsuario, Postagem
from django.contrib.auth.forms import PasswordResetForm
from django import forms
from .models import Tarefa

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['nome', 'descricao']  # Incluir todos os campos do modelo que deseja manipular

# Formulário para perfil de usuário
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['foto_perfil', 'nome', 'sobrenome', 'bio', 'email']  # Campos de perfil

# Formulário para edição do perfil
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nome', 'sobrenome', 'foto_perfil']  # Ajustado para CustomUser

# Formulário para editar o perfil do usuário
class EditPerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['foto_perfil', 'bio']  # Perfil do usuário, sem campos duplicados

# Formulário para CustomUser
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nome', 'bio', 'foto_perfil']  # Campos ajustados

# Formulário para atualizar informações do usuário
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nome', 'sobrenome', 'email', 'bio', 'room', 'foto_perfil']  # Campos incluídos

# Formulário para o modelo Postagem
class PostagemForm(forms.ModelForm):
    class Meta:
        model = Postagem
        fields = ['texto', 'imagem']
        widgets = {
            'texto': forms.Textarea(attrs={'placeholder': 'Digite sua mensagem...'}),
            'imagem': forms.FileInput(),
        }

# Formulário personalizado para redefinição de senha
class CustomPasswordResetForm(PasswordResetForm):
    class Meta:
        model = CustomUser
        fields = ['email']
