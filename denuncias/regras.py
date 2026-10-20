def eh_dona(user, denuncia):
    """True se a denúncia foi registrada por este usuário."""
    return denuncia.denunciante_id == user.id


def pode_ver_denuncia(user, denuncia):
    """CAE (permissão view_denuncia) ou a própria dona da denúncia."""
    return user.has_perm('denuncias.view_denuncia') or eh_dona(user, denuncia)