from celery import shared_task
from Crypto.PublicKey import RSA
from django.conf import settings
from django.core.files.base import ContentFile

from spaces.models import File, Space
from spaces.utils import encrypt


def sync_encrypt_and_save(user_id, file_id):
    user_space = Space.objects.get(user=user_id)
    key = user_space.public_key
    public_key = RSA.import_key(key)

    file_instance = File.objects.get(id=file_id)
    encrypted_data = encrypt(file_instance.data, public_key)
    file_instance.data = encrypted_data
    file_instance.end = True
    file_instance.save()
    return True


@shared_task
def async_encrypt_and_save(user_id, file_id):
    return sync_encrypt_and_save(user_id, file_id)


def encrypt_and_save(user_id,  file_id):
    if not settings.CELERY:
        return sync_encrypt_and_save(user_id, file_id)
    else:
        return async_encrypt_and_save.delay(user_id, file_id)
