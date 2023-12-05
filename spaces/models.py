from django.db import models
from django.dispatch import receiver

from .utils import generate_keys


class Space(models.Model):
    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="space"
    )
    private_key = models.BinaryField()
    public_key = models.BinaryField()

    def __str__(self):
        return self.user.username


class File(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    name = models.TextField()
    file = models.FileField(upload_to="files/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ended = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# create space when user created
@receiver(models.signals.post_save, sender="auth.User")
def create_space(sender, instance, created, **kwargs):
    if created:
        try:
            public_key, private_key = generate_keys()
            pb_key = public_key.export_key("PEM")
            pr_key = private_key.export_key("PEM")
            Space.objects.create(user=instance, private_key=pr_key, public_key=pb_key)
        except:
            instance.delete()
