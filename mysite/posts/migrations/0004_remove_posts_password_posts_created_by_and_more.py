# Generated by Django 5.1.4 on 2025-01-13 01:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0003_alter_posts_original_filename"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="posts",
            name="password",
        ),
        migrations.AddField(
            model_name="posts",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posts_created_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AddField(
            model_name="posts",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posts_updated_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
    ]
