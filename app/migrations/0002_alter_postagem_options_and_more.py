# Generated by Django 5.1.2 on 2024-11-05 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postagem',
            options={'verbose_name_plural': 'Postagens'},
        ),
        migrations.RenameField(
            model_name='curtida',
            old_name='desenho',
            new_name='postagem',
        ),
        migrations.RenameField(
            model_name='postagem',
            old_name='descricao',
            new_name='texto',
        ),
        migrations.RemoveField(
            model_name='postagem',
            name='categoria',
        ),
        migrations.RemoveField(
            model_name='postagem',
            name='titulo',
        ),
        migrations.AlterField(
            model_name='postagem',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='desenhos/'),
        ),
    ]
