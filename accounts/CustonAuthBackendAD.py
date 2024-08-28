# -*- coding: utf-8 -*-

from django.contrib.auth.models import User


class AzureauthBackend():
    def authenticate(self, request, username, password, win):
        try:
            user = User.objects.get(username=username)
            success = User.check_password(password)
            if success:
                return user
        except User.DoesNotExist:
            user = User(username=username)
            user.email = win['mail'] 
            user.first_name = win['surname'] 
            user.last_name = win['mail'] 
            user.is_staff = True
            user.set_password('mude_aqui')
            user.win.winID = win['id']
            user.win.jobTitle = win['jobTitle']
            user.win.token = "token incial"
            user.save()
            return user
        return None
    
    def get_user(self, uid):
        try:
            return User.objects.get(pk=uid)
        except:
            return None