# Generated by Django 2.1.1 on 2018-09-19 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rank_me_api', '0013_auto_20180919_0549'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradeitem',
            name='status_text',
            field=models.CharField(default='empy\x08ty\\\x08\x08\x08\x08\x08', max_length=255),
            preserve_default=False,
        ),
    ]
