from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, pre_save ,  pre_delete
from django.dispatch import receiver

User._meta.get_field('email')._unique = True

class Win(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    jobTitle = models.CharField(max_length=250)
    winID = models.CharField(max_length=250)
    token = models.TextField()

@receiver(post_save, sender = User)
def create_user_win(sender, instance, created,**kwargs):
    if created:
        Win.objects.create(user=instance)
        
# =============================================================================
# @receiver(post_save, sender = User)
# def save_user_win(sender, instance,**kwargs):
#         instance.win.save()
# =============================================================================



class Team(models.Model):
    name = models.CharField(max_length=80)
    owner = models.ForeignKey(User,on_delete = models.PROTECT)
    def __str__(self) :
        return self.name
    ## add owner 

class Function(Group):
    title = models.CharField(max_length=250)
    team = models.ForeignKey(Team,on_delete = models.CASCADE)


class Member(models.Model):
    user = models.ForeignKey(User,on_delete = models.PROTECT)
    function = models.ForeignKey(Function,on_delete = models.CASCADE)


@receiver(pre_save, sender = Function)
def create_function(sender, instance,**kwargs):
    instance.name = instance.title +'_'+ instance.team.name
    

@receiver(pre_save, sender = Member)
def change_menber(sender, instance,**kwargs):
    if instance.id:
        old = Member.objects.get(pk = instance.pk)
        instance.user.groups.remove(old.function)
    instance.user.groups.add(instance.function)

@receiver(pre_delete, sender = Member)
def delete_menber(sender, instance,**kwargs):
    if instance.id:
        old = Member.objects.get(pk = instance.pk)
        instance.user.groups.remove(old.function)
       