# Generated by Django 4.1.7 on 2023-04-06 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_chat_participants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='chats', to='chat.contact'),
        ),
    ]
