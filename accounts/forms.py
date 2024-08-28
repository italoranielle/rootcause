# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.contrib.auth.models import User , Permission 
from .models import Function, Team , Member
from django.db.models import Q 
from django.contrib.auth.forms import UserCreationForm

LIST_PERMS = ('add_analysis',
'delete_analysis',
'change_analysis',
'view_analysis',
'add_w5h2',
'view_w5h2',
'change_w5h2',
'view_ishikawa',
'add_ishikawa',
'change_ishikawa',
'add_pqs5',
'view_pqs5',
'delete_pqs5',
'view_acao',
'add_acao',
'change_acao',
'delete_acao',
'change_team',
'add_member',
'delete_member',
'change_member')

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class profileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name'] 
        
class userAdminForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email','user_permissions','is_active']

class FunctionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('current_user')
        super(FunctionForm, self).__init__(*args, **kwargs)
        # access object through self.instance...
        self.fields['team'].queryset = Team.objects.filter(Q(function__member__user = user) | Q(owner= user) ).distinct()
        self.fields['permissions'].queryset = Permission.objects.filter(codename__in=LIST_PERMS)
    class Meta:
        model = Function
        exclude = ('name',)
        help_texts = {
            'permissions': ('Pressione “Control”, ou “Command” no Mac, para selecionar mais de um).'),
        }

class MemberForm(ModelForm):
    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team_')
        super(MemberForm, self).__init__(*args, **kwargs)
        # access object through self.instance...
        self.fields['function'].queryset = Function.objects.filter(team=team)

    class Meta:
        model = Member
        fields= ('function',)