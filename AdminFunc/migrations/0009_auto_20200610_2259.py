# Generated by Django 3.0.5 on 2020-06-10 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AdminFunc', '0008_auto_20200610_0152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjects',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]