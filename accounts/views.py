from django.shortcuts import render, redirect
from django.contrib.auth.forms import  PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User , Permission 
from .models import Team, Function , Member
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .forms import profileForm ,userAdminForm , FunctionForm , MemberForm , SignUpForm
from django.views.generic import UpdateView ,CreateView ,DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin ,UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from .graph_helper import get_user, get_calendar_events
from django.http import JsonResponse
from django.db.models import Q
from aqf.funcs import is_in_team_and_has_permission





class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
    
@login_required    
def UserView(request):
    user = User.objects.filter(pk = request.user.pk)
    data = {'usuario':user } 
    
    if request.method =='POST':
        form = UserChangeForm(request.POST, instance=request.use)
        if form.is_valid():
            form.save()
    return render(request, 'accounts/profile.html',data) 


@permission_required('auth.view_user')
def Userlist(request):
    user = User.objects.all()
    data = {'usuario':user }  
    return render(request, 'accounts/userList.html',data) 


@login_required 
def PasswordReset(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('change_password')
        else:
            messages.error(request, 'Erro! Tente novamente.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/resetUser.html', {'form': form})
    
@login_required
def Update(request):
    if request.method == 'POST':
        form = profileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = profileForm(instance=request.user)

    return render(request, 'accounts/update.html', {'form': form})


class UpdateAdmin(PermissionRequiredMixin,UpdateView):
    model = User
    form_class = userAdminForm
    template_name = 'accounts/update.html'
    permission_required = 'auth.change_user'
    success_url = reverse_lazy('list_user')
    
def TeamView(request):
    teams = Team.objects.filter(Q(function__member__user = request.user) | Q(owner= request.user) ).distinct()
    functions = Function.objects.filter(team__in = teams)
    members = Member.objects.filter(function__in = functions)

    data = {'teams':teams,'functions':functions, 'members':members,}
    return render(request, 'team/list.html',data)  


def addMember(request):
    if request.method == 'POST':
        user = User.objects.get(email= request.POST.get('mail'))
        function = Function.objects.get(pk= request.POST.get('function'))
        Member(user=user,function=function).save()
        return JsonResponse({'msg':'saved'})
    else:
        team = request.GET.get('team')
        functions = Function.objects.filter(team=team)
        if not is_in_team_and_has_permission(request.user,team,'accounts.add_member'):
            raise PermissionDenied("Você não pode adicionar mebros nesse time")
        return render(request, 'team/member_form.html',{'functions':functions})

class RemoveMember(UserPassesTestMixin,DeleteView):
    model = Member
    template_name = 'team/delete.html'
    success_url = reverse_lazy('myteams')
    permission_denied_message = 'Você não pode remover membros desse time!'

    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().function.team.pk,'accounts.delete_member')
    

class UpdateMember(UserPassesTestMixin,UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'team/form.html'
    permission_denied_message = 'Você não pode alterar membros desse time!'

    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().function.team.pk,'accounts.change_member')

    def get_form_kwargs(self):
        kwargs = super(UpdateMember, self).get_form_kwargs()
        kwargs['team_'] = Team.objects.get(function = self.get_object().function )
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit = False)
        obj.save()
        return JsonResponse({'msg':'saved'})

class CreateTeam(CreateView):
    model = Team
    fields = ('name',)
    template_name = 'team/form.html'
    success_url = reverse_lazy('myteams')

    def form_valid(self, form):
        obj = form.save(commit = False)
        obj.owner = self.request.user
        obj.save()
        return JsonResponse({'msg':'saved'})
        
class CreateFunction(UserPassesTestMixin,CreateView):
    model = Function
    form_class = FunctionForm
    template_name = 'team/form.html'
    permission_denied_message = 'Você não pode alterar esse time!'

    def test_func(self):
        team = self.request.POST.get('team') if self.request.GET.get('team',None) is None else self.request.GET.get('team',None)
        return is_in_team_and_has_permission(self.request.user,team,'accounts.change_team')

    def get_form_kwargs(self):
        kwargs = super(CreateFunction, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs

    def get_initial(self):
        team= self.request.GET.get('team',None)
        if  team :
            data = { 'team': Team.objects.get(pk = team) }
            return data

    def form_valid(self, form):
        obj = form.save(commit = False)
        permissions = Permission.objects.filter(pk__in= self.request.POST.getlist('permissions'))
        obj.save()
        for perm in permissions :
            print(perm)
            obj.permissions.add(perm)
        obj.save()
        return JsonResponse({'msg':'saved'})

class UpdateFunction(UserPassesTestMixin,UpdateView):
    model = Function
    form_class = FunctionForm
    template_name = 'team/form.html'
    permission_denied_message = 'Você não pode alterar esse time!'

    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().team.pk,'accounts.change_team')

    def get_form_kwargs(self):
        kwargs = super(UpdateFunction, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit = False)
        permissions = Permission.objects.filter(pk__in= self.request.POST.getlist('permissions'))
        obj.permissions.clear()
        for perm in permissions :
            obj.permissions.add(perm)
        obj.save()
        return JsonResponse({'msg':'saved'})


class FunctionDelete(UserPassesTestMixin,DeleteView):
    model = Function
    template_name = 'team/delete.html'
    success_url = reverse_lazy('myteams')
    permission_denied_message = 'Você não pode alterar esse time!'

    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().team.pk,'accounts.change_team')


def initialize_context(request):
  context = {}
  error = request.session.pop('flash_error', None)
  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context

def win_login(request):
  sign_in_url, state = get_sign_in_url()
  request.session['auth_state'] = state
  return reverse_lazy(sign_in_url)
   

def callback(request):

  expected_state = request.session.pop('auth_state', '')
 
  token = get_token_from_code(request.get_full_path(), expected_state)

  user = get_user(token)
  
 
  store_token(request, token)
  store_user(request, user)

  return reverse_lazy('home')



