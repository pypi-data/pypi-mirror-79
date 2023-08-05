# Generated by Django 2.1.11 on 2019-08-30 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('terra_geocrud', '0008_crudview_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crudview',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='crud_views', to='template_model.Template'),
        ),
    ]
