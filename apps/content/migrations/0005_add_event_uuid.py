import uuid
from django.db import migrations, models

def gen_uuid(apps, schema_editor):
    Event = apps.get_model('content', 'Event')
    for row in Event.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=['uuid'])

class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_eventregistration'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='event',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
