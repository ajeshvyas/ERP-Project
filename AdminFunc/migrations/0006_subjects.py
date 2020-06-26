# Generated by Django 3.0.5 on 2020-06-09 15:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AdminFunc', '0005_auto_20200609_2100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=40)),
                ('weightage', models.DecimalField(decimal_places=2, max_digits=4)),
                ('added_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('class_assigned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminFunc.Classes')),
            ],
        ),
    ]