# Generated by Django 5.1 on 2024-08-30 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_postmodel_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postmodel',
            old_name='product_id',
            new_name='postId',
        ),
    ]
