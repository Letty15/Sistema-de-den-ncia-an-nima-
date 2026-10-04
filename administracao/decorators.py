from django.contrib.auth.decorators import login_required, user_passes_test


def eh_cae(user):
    """Confere se o usuário logado pertence ao grupo CAE."""
    return user.is_authenticated and user.groups.filter(name='CAE').exists()


def cae_required(view_func):
    """Decorator único: exige login E pertencer ao grupo CAE."""
    return login_required(user_passes_test(eh_cae, login_url='login')(view_func))