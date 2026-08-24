from django.db import migrations

def criar_grupo(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='CAE')

def remover_grupo(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='CAE').delete()

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(criar_grupo, remover_grupo),
    ]