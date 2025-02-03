# Generated by Django 5.1.4 on 2025-01-29 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('python_blog', '0002_tag_remove_post_tags_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('review', 'На проверке'), ('reviewed', 'Проверено'), ('published', 'Опубликовано')], default='review', max_length=10, verbose_name='Статус'),
        ),
    ]
