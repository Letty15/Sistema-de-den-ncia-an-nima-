from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('denuncias', '0003_alter_denuncia_protocolo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='denuncia',
            options={'permissions': [('alterar_status_denuncia', 'Pode alterar o status da denúncia')]},
        ),
    ]