from django.db import migrations

CODENAME = 'alterar_status_denuncia'
NOME = 'Pode alterar o status da denúncia'


def dar_permissao_a_cae(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Permission = apps.get_model('auth', 'Permission')
    Group = apps.get_model('auth', 'Group')

    # A permissão só seria criada no fim do migrate; criamos agora para
    # poder atribuí-la ao grupo (o Django reaproveita o registro depois).
    tipo, _ = ContentType.objects.get_or_create(app_label='denuncias', model='denuncia')
    permissao, _ = Permission.objects.get_or_create(
        content_type=tipo, codename=CODENAME, defaults={'name': NOME},
    )
    cae, _ = Group.objects.get_or_create(name='CAE')
    cae.permissions.add(permissao)


def tirar_permissao_da_cae(apps, schema_editor):
    Permission = apps.get_model('auth', 'Permission')
    Group = apps.get_model('auth', 'Group')
    permissao = Permission.objects.filter(
        codename=CODENAME, content_type__app_label='denuncias',
    ).first()
    cae = Group.objects.filter(name='CAE').first()
    if permissao and cae:
        cae.permissions.remove(permissao)


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('administracao', '0002_grupos_e_permissoes'),
        ('denuncias', '0004_permissao_alterar_status'),
    ]

    operations = [
        migrations.RunPython(dar_permissao_a_cae, tirar_permissao_da_cae),
    ]