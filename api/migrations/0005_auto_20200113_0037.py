# Generated by Django 2.2.9 on 2020-01-13 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_apartment_occupied'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='bookedapartment',
            name='occupied',
            field=models.BooleanField(default=False),
        ),
    ]
