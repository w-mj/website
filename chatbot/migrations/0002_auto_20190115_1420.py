# Generated by Django 2.1.5 on 2019-01-15 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chathistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_history', to=settings.AUTH_USER_MODEL),
        ),
    ]