# Generated by Django 4.1.7 on 2023-04-18 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_room_slot_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='targeted_level',
            field=models.IntegerField(default=0),
        ),
    ]
