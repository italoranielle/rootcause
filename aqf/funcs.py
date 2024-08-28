from accounts.models import Team
from django.db.models import Q 
#Team.objects.filter(Q(function__member__user = user) | Q(owner= user) ).distinct()

def is_in_team_and_has_permission(user,team_pk,permission):
    team =Team.objects.get(pk=team_pk)
    teams = Team.objects.filter(Q(function__member__user = user) | Q(owner= user) ).distinct()
    if team in teams:
        if user.has_perm(permission) or user == team.owner or user.is_superuser or user.is_staff  :
            return True
    return False
