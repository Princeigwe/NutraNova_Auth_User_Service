# Generated by Django 4.2.5 on 2023-10-25 17:28

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_customuser_allergens'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='allergens',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('MILK', 'milk'), ('EGG', 'egg'), ('PEANUT', 'peanut'), ('SOY', 'soy'), ('WHEAT', 'wheat'), ('TREE_NUTS', 'tree nuts'), ('SHELLFISH', 'shellfish'), ('SESAME', 'sesame'), ('GARLIC', 'garlic')], max_length=50),
        ),
    ]
