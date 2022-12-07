# Generated by Django 4.0.3 on 2022-11-23 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import myApp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to=myApp.models.get_upload_path)),
                ('content', models.TextField(default='none')),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(to='accounts.g')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]