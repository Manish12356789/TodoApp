from django.db import models
from django.contrib.auth.models import User, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    field = models.CharField(max_length=60)
    status = models.CharField(max_length=50, default="remaining")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Items"

    def __str__(self):
        return self.field


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True, default="default.jpg")

    def __str__(self):
        return self.user.username


# class UserInstanceProfile(User):
#     class Meta:
#         proxy = True
#         user_name = ('username',)
#
#         def __str__(self):
#             return self.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_artist(sender, instance, **kwargs):
#     instance.user.save()
