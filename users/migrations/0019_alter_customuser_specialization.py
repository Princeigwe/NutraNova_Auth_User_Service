# Generated by Django 4.2.5 on 2024-06-05 17:58

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_customuser_dietary_preference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='specialization',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('GENERAL', 'General Nutrition'), ('SPORTS', 'Sports Nutrition'), ('PEDIATRIC', 'Pediatric'), ('WEIGHT_LOSS', 'Weight Loss'), ('DIABETICS', 'Diabetics'), ('HEART_HEALTH', 'Heart Health'), ('GASTROENTEROLOGY', 'Gastroenterology'), ('ONCOLOGY', 'Oncology'), ('RENAL', 'Renal Nutrition'), ('VEGAN', 'Vegan and Vegetarian Nutrition'), ('FOOD_ALLERGIES', 'Food Allergies and Intolerance'), ('GERIATRICS', 'Geriatric Nutrition'), ('PREGNANCY', 'Pregnancy and Prenatal Nutrition'), ('POSTPARTUM', 'Postpartum Nutrition'), ('EATING_DISORDERS', 'Eating Disorders'), ('MEAL_PLANNING', 'Meal Planning'), ('CULINARY', 'Culinary Nutrition'), ('NUTRITIONAL_SUPPLEMENTS', 'Nutritional Supplements'), ('PUBLIC_HEALTH', 'Public Health Nutrition'), ('WEIGHT_GAIN', 'Healthy Weight Gain')], max_length=50, null=True),
        ),
    ]
