# Generated manually to support JOIN job synchronization.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_contactmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='external_id',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='job',
            name='source_status',
            field=models.CharField(blank=True, default='ONLINE', max_length=20),
        ),
        migrations.AddField(
            model_name='job',
            name='raw_data',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
