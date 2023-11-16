# Generated by Django 4.2.5 on 2023-10-26 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_customuser_availability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='professional_statement',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='specialization',
            field=models.CharField(blank=True, choices=[('GENERAL', 'General Nutrition'), ('SPORTS', 'Sports Nutrition'), ('PEDIATRIC', 'Pediatric'), ('WEIGHT_LOSS', 'Weight Loss'), ('DIABETICS', 'Diabetics'), ('HEART_HEALTH', 'Heart Health'), ('GASTROENTEROLOGY', 'Gastroenterology'), ('ONCOLOGY', 'Oncology'), ('RENAL', 'Renal Nutrition'), ('VEGAN', 'Vegan and Vegetarian Nutrition'), ('FOOD_ALLERGIES', 'Food Allergies and Intolerance'), ('GERIATRICS', 'Geriatric Nutrition'), ('PREGNANCY', 'Pregnancy and Prenatal Nutrition'), ('POSTPARTUM', 'Postpartum Nutrition'), ('EATING_DISORDERS', 'Eating Disorders'), ('MEAL_PLANNING', 'Meal Planning'), ('CULINARY', 'Culinary Nutrition'), ('NUTRITIONAL_SUPPLEMENTS', 'Nutritional Supplements'), ('PUBLIC_HEALTH', 'Public Health Nutrition'), ('WEIGHT_GAIN', 'Healthy Weight Gain')], max_length=50, null=True),
        ),
    ]
