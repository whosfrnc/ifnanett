from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

# Modelo de Categorias
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome

# Gerenciador de Usuários Customizado
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Modelo Customizado de Usuário
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    nome = models.CharField(max_length=30, blank=True)
    sobrenome = models.CharField(max_length=30, blank=True)
    room = models.CharField(max_length=255, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# Modelo de Perfil de Usuário (duplicidade removida)
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Perfis de Usuários'

    def __str__(self):
        return self.nome

# Modelo de Logs de Acesso
class LogAcesso(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    data_acesso = models.DateTimeField(auto_now_add=True)
    endereco_ip = models.GenericIPAddressField()

    class Meta:
        verbose_name_plural = 'Logs de Acesso'

    def __str__(self):
        return f'{self.usuario.nome} - {self.data_acesso}'

# Modelo de Postagem (anteriormente Desenho)
class Postagem(models.Model):
    titulo = models.CharField(max_length=255, default="Título Padrão", blank=False)
    texto = models.TextField(null=True, blank=True)  # Campo de texto opcional
    imagem = models.ImageField(upload_to='desenhos/', null=True, blank=True)  # Campo de imagem opcional
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curtidas = models.ManyToManyField(get_user_model(), related_name='curtidas', blank=True)
    data_publicacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Postagens'
        
    def total_curtidas(self):
        return self.curtidas.count() 

    def __str__(self):
        return f"{self.usuario.username} - {self.data_publicacao.strftime('%Y-%m-%d %H:%M')}"
    
    
# Modelo de Suporte
class Suporte(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assunto = models.CharField(max_length=255)
    mensagem = models.TextField()
    data_criacao = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, choices=[('aberto', 'Aberto'), ('em andamento', 'Em andamento'), ('fechado', 'Fechado')], default='aberto')

    class Meta:
        verbose_name_plural = 'Suporte'

    def __str__(self):
        return f'{self.assunto} - {self.status}'

# Modelo de Curtida
class Curtida(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE)
    data_curtida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Curtidas'

    def __str__(self):
        return f'{self.usuario.nome} - {self.postagem.titulo}'

# Modelo de Comentário
class Comentario(models.Model):
    postagem = models.ForeignKey('Postagem', on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nome}: {self.conteudo}"
    
class Tarefa(models.Model):
    nome = models.CharField(max_length=200)
    criado_em = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Relacionamento com o usuário logado

    def __str__(self):
        return self.nome