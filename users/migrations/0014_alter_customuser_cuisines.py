# Generated by Django 4.2.5 on 2023-11-19 17:13

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cuisines',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('ITALIAN', 'Italian'), ('MEDITERRANEAN', 'Mediterranean'), ('ASIAN', 'Asian'), ('MEXICAN', 'Mexican'), ('MIDDLE_EASTERN', 'Middle Eastern'), ('AMERICAN', 'American'), ('FRENCH', 'French'), ('INDIAN', 'Indian'), ('AFRICAN', 'African')], default='ITALIAN', max_length=50),
        ),
    ]
