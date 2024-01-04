from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile
from django.conf import settings


def createProfile(sender,instance,created, **kwargs):
    print("profile Trigger")
    if(created):
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = "",
            phone = "",
        )
        profile.save()


def updateUser(sender,instance,created,**kwargs):
    profile = instance
    print("update Trigger")
    print(profile)
    user = profile.user
    if created == False:
        user.username = profile.username
        user.email = profile.email
        user.save()



post_save.connect(updateUser,sender=Profile)
post_save.connect(createProfile,sender=User)