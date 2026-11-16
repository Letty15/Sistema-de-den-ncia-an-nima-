import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conteudos', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conteudoeducativo',
            name='autor',
            field=models.ForeignKey(
                limit_choices_to={'groups__name': 'CAE'},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]