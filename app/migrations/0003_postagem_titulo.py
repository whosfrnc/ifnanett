# Generated by Django 5.1.2 on 2024-11-05 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_postagem_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='postagem',
            name='titulo',
            field=models.CharField(default=' ', max_length=255),
            preserve_default=False,
        ),
    ]