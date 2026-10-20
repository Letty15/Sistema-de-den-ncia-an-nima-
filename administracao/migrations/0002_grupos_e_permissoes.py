from django.contrib.auth.management import create_permissions
from django.db import migrations

PERMISSOES_CAE = [
    'view_denuncia',
    'add_conteudoeducativo', 'change_conteudoeducativo',
    'delete_conteudoeducativo', 'view_conteudoeducativo',
    'add_canalapoio', 'change_canalapoio',
    'delete_canalapoio', 'view_canalapoio',
    'add_respostadenuncia', 'change_respostadenuncia',
    'delete_respostadenuncia', 'view_respostadenuncia',
    'view_usuario', 'change_usuario', 'delete_usuario',
]

PERMISSOES_DENUNCIANTE = [
    'add_denuncia', 'change_denuncia', 'delete_denuncia',
    'view_respostadenuncia',
]


def criar_grupos_e_permissoes(apps, schema_editor):
    # O Django só cria as permissões no fim do migrate.
    # Aqui forçamos a criação agora, para poder atribuí-las.
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    User = apps.get_model('auth', 'User')
    Usuario = apps.get_model('usuarios', 'Usuario')

    cae, _ = Group.objects.get_or_create(name='CAE')
    denunciante, _ = Group.objects.get_or_create(name='Denunciante')

    cae.permissions.set(Permission.objects.filter(codename__in=PERMISSOES_CAE))
    denunciante.permissions.set(Permission.objects.filter(codename__in=PERMISSOES_DENUNCIANTE))

    # contas que já existiam e não são CAE entram no grupo Denunciante
    ids = list(Usuario.objects.values_list('pk', flat=True))
    for user in User.objects.filter(pk__in=ids).exclude(groups=cae):
        user.groups.add(denunciante)


def desfazer(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    cae = Group.objects.filter(name='CAE').first()
    if cae:
        cae.permissions.clear()
    Group.objects.filter(name='Denunciante').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('administracao', '0001_criar_grupo_cae'),
        ('denuncias', '0003_alter_denuncia_protocolo'),
        ('conteudos', '0002_initial'),
        ('respostas', '0002_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(criar_grupos_e_permissoes, desfazer),
    ]