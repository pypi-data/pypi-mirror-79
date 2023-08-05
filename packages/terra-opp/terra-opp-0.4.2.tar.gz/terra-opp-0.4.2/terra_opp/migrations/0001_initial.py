# Generated by Django 2.2.5 on 2019-10-09 09:24

from django.conf import settings
try:
    from django.db.models import JSONField
except ImportError:  # TODO Remove when dropping Django releases < 3.1
    from django.contrib.postgres.fields import JSONField
from django.db import migrations, models
import django.db.models.deletion
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geostore', '0029_auto_20190926_0803'),
    ]

    operations = [
        migrations.CreateModel(
            name='Viewpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(max_length=100, verbose_name='Label')),
                ('properties', JSONField(blank=True, default=dict, verbose_name='Properties')),
                ('point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points', to='geostore.Feature')),
            ],
            options={
                'ordering': ['-created_at'],
                'permissions': (('can_download_pdf', 'Is able to download a pdf document'),),
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('state', models.IntegerField(default=100, verbose_name='State')),
                ('properties', JSONField(blank=True, default=dict, verbose_name='Properties')),
                ('file', versatileimagefield.fields.VersatileImageField(upload_to='', verbose_name='File')),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('remarks', models.TextField(max_length=350, verbose_name='Remarks')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pictures', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('viewpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='terra_opp.Viewpoint')),
            ],
            options={
                'ordering': ['-date'],
                'permissions': (('change_state_picture', 'Is able to change the picture state'),),
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(max_length=100, verbose_name='Label')),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assigned_campaigns', to=settings.AUTH_USER_MODEL, verbose_name='Assigned to')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='campaigns', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
                ('viewpoints', models.ManyToManyField(related_name='campaigns', to='terra_opp.Viewpoint')),
            ],
            options={
                'ordering': ['-created_at'],
                'permissions': (('manage_all_campaigns', 'Can manage all campaigns'),),
            },
        ),
        migrations.AddIndex(
            model_name='picture',
            index=models.Index(fields=['viewpoint', 'date'], name='terra_opp_p_viewpoi_bbead9_idx'),
        ),
    ]
