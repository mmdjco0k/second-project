# Generated by Django 5.1 on 2024-08-30 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_rename_product_id_postmodel_postid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postmodel',
            old_name='postId',
            new_name='product_id',
        ),
    ]
