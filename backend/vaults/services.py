from django.contrib.auth.models import User
from django.db import transaction

from .models import Vault


@transaction.atomic
def vault_create(*, name: str, user: User) -> Vault:
    vault = Vault.objects.create(
        name=name,
        user=user,
    )

    return vault


@transaction.atomic
def vault_update(*, vault: Vault, name: str) -> Vault:
    vault.name = name
    vault.full_clean()

    vault.save()
    return vault


@transaction.atomic
def vault_delete(*, vault: Vault) -> None:
    vault.delete()
