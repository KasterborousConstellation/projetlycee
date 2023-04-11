# Generated by Django 4.1.7 on 2023-04-09 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matiere', models.CharField(max_length=20)),
                ('heure', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='day',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='class',
            name='month',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='student',
            name='genre',
            field=models.CharField(default='M', max_length=1),
        ),
        migrations.AlterField(
            model_name='class',
            name='places',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='class',
            name='slot',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='login.slot'),
        ),
    ]