from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


def Custom_upload_to(instance, filename):
    old_instance = Profile(pk=instance.pk)
    old_instance.avatar.delete
    return 'profiles/' + filename
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=Custom_upload_to, null=True, blank=True)
    bio = models.TextField()
    link = models.URLField(max_length=200,null=True, blank=True)

    class Meta:
        ordering = ['user__username']

    @receiver(post_save, sender=User)
    def Ensurace_profile_exist(sender, instance, **kwargs):
        if kwargs.get('created', False):
            Profile.objects.get_or_create(user=instance)