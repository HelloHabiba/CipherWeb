from celery import shared_task
from Crypto.PublicKey import RSA
from django.conf import settings
from django.core.files.base import ContentFile

from spaces.models import File, Space
from spaces.utils import encrypt


def sync_encrypt_and_save(user_id, clean_file, file_id):
    user_space = Space.objects.get(user=user_id)
    key = user_space.public_key
    public_key = RSA.import_key(key)

    file_instance = File.objects.get(id=file_id)
    encrypted_data = encrypt(clean_file, public_key)
    file_data = ContentFile(encrypted_data, name=file_instance.name)
    file_instance.file = file_data
    file_instance.ended = True
    file_instance.save()
    return True


@shared_task
def async_encrypt_and_save(user_id, clean_file, file_id):
    return sync_encrypt_and_save(user_id, clean_file, file_id)


def encrypt_and_save(user_id, clean_file, file_id):
    if not settings.CELERY:
        return sync_encrypt_and_save(user_id, clean_file, file_id)
    else:
        return async_encrypt_and_save.delay(user_id, clean_file, file_id)
