from django.shortcuts import render , redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView,DetailView,UpdateView ,DeleteView
from django.views.generic.edit import CreateView
from . models import W5h2 , Pqs5 , Ishikawa, Acao , Analysis , Bucket , Shift ,Area
from .forms import AnalysisForm, Psq5Form, IshikawaForm , AcaoForm , W5h2Form, AreaForm , ShiftForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.forms.models import model_to_dict
from accounts.models import Team
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import  RestrictedError 
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from .funcs import is_in_team_and_has_permission


"""
class RaiSearchView(ListView):
    model = Rai
    template_name = 'aqf/rai_view.html'

    def get_queryset(self):
        try:
            search = self.request.GET.get('q')
        except:
            search = ''
        try:
            search = int(search)
            object_list = Rai.objects.filter(Q(ordem=int(search)))
        except:
            if (search != ''):
                object_list = Rai.objects.filter(Q(fenomenos__icontains = search) | Q(maquina__icontains = search) )
            else:
                object_list = Rai.objects.all()
        return object_list
"""  
def dinamicMenu(analysis):
    analysis = Analysis.objects.get(pk=analysis)
    menu = """
    <li class="nav-item">
        <a class="nav-link" href="{}">
          <i class="fas fa-fw fa-file-medical"></i>
          <span>Nova Analise</span></a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="{}">
          <i class="fas fa-fw fa-file-alt"></i>
          <span>Analise</span>
         </a>
    </li>   
    """.format(reverse('analysis_new'),reverse('analysis_detail',args=[analysis.pk]))
    if analysis.do_w5h2:
        try:
            W5h2.objects.get(analysis= analysis)
            url = reverse('w5h2_edit',args=[analysis.w5h2.pk])
        except :
            url = reverse('w5h2_new',args=[analysis.pk])
        menu += """
        <li class="nav-item">
        <a class="nav-link" href="{}">
          <i class="fas fa-fw fa-file-alt"></i>
          <span>5W2H</span>
         </a>
        </li>
        """.format(url)
    if analysis.do_ishikawa:
        menu += """
        <li class="nav-item">
        <a class="nav-link" href="{}">
          <i class="fas fa-fw fa-fishbone"></i>
          <span> Ishikawa</span>
         </a>
        </li>
        """.format(reverse('ishikawa_view',args=[analysis.pk]))
    if analysis.do_whays:
        menu += """
       <li class="nav-item">
        <a class="nav-link" href="{}">
          <i class="fas fa-fw fa-pq5"></i>
          <span> 5PQ's</span>
         </a>
        </li>
        """.format(reverse('pqs5_list',args=[analysis.pk]))
    if analysis.do_action_plan:
        menu += """
       <li class="nav-item">
        <a class="nav-link" href="{}">
          <i class="fas fa-fw fa-user-cog"></i>
          <span>Plano de Ação</span>
         </a>
        </li>
        """.format(reverse('kamban',args=[analysis.pk]))
    return menu

def home(request):
    return render(request,'home.html')

# ----------------------------Analisys--------------------------
class AnalysisList(LoginRequiredMixin,ListView):
    model = Analysis
    template_name = 'analysis/list.html'

    def get_context_data(self, **kwargs):
        context = super(AnalysisList ,self).get_context_data(**kwargs)
        context['alert']= False if Team.objects.filter(Q(function__member__user = self.request.user) | Q(owner= self.request.user)  ).count() > 0 else True
        return context

    def get_queryset(self):
        meusTeams = Team.objects.filter(Q(function__member__user = self.request.user) | Q(owner= self.request.user)  ).distinct()
        object_list = Analysis.objects.filter(Q(team__in= meusTeams))
        return object_list


class AnalysisCreateView(LoginRequiredMixin,CreateView):  
    model =  Analysis
    template_name = 'analysis/form.html'
    form_class = AnalysisForm
    
    def form_valid(self , form):
        obj = form.save(commit = False)
        obj.created_by = self.request.user
        if not is_in_team_and_has_permission(self.request.user,obj.team.pk,'aqf.add_analysis'):
            raise PermissionDenied("Você não pode adicionar analise! Você não faz parte do time ou não tem a permição nescessaria")
        obj.save()
        return super().form_valid(form) 
    
    def get_context_data(self, **kwargs):
        context = super(AnalysisCreateView ,self).get_context_data(**kwargs)
        teams = Team.objects.filter(Q(function__member__user = self.request.user) | Q(owner= self.request.user) ).distinct().values_list('pk',flat=True)
        context['team_related'] = {team:{ 'area':list(Area.objects.filter(team_id= team).values_list(flat=True)),
                                      'turno':list(Shift.objects.filter(team_id= team).values_list(flat=True)) ,
                                      'membro':list(User.objects.filter(member__function__team = team).values_list(flat=True))
                                        } for team in teams}
        return context

    def get_form_kwargs(self):
        kwargs = super(AnalysisCreateView, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs


class AnalysisDeleteView(UserPassesTestMixin,DeleteView):
    model = Analysis
    template_name = 'generic/delete.html'
    success_url = reverse_lazy('analysis_list')
    permission_denied_message = 'Você não pode Deletar essa analise! Você não faz parte do time ou não tem a permição nescessaria'

    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().team.pk,'aqf.delete_analysis') 




class AnalysisUpdate(UserPassesTestMixin,UpdateView):
    model =  Analysis
    template_name = 'analysis/form.html'
    form_class = AnalysisForm
    permission_denied_message = 'Você não pode alterar essa analise! Você não faz parte do time ou não tem a permição nescessaria'
    
    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().team.pk,'aqf.change_analysis') 

    def get_context_data(self, **kwargs):
        context = super(AnalysisUpdate ,self).get_context_data(**kwargs)
        teams = Team.objects.filter(Q(function__member__user = self.request.user) | Q(owner= self.request.user) ).distinct().values_list('pk',flat=True)
        context['team_related'] = {team:{ 'area':list(Area.objects.filter(team_id= team).values_list(flat=True)),
                                      'turno':list(Shift.objects.filter(team_id= team).values_list(flat=True)) ,
                                      'membro':list(User.objects.filter(member__function__team = team).values_list(flat=True))
                                        } for team in teams}
        return context
        

    def get_form_kwargs(self):
        kwargs = super(AnalysisUpdate, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs



class AnalysisDetailView(UserPassesTestMixin,DetailView):
    model =  Analysis
    template_name = 'analysis/detail.html'
    permission_denied_message = 'Você não pode vizualizar essa analise! Você não tem a permição nescessaria ou não faz parte do time'
    
    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().team.pk,'aqf.view_analysis') 

    def get_context_data(self, **kwargs):
        context = super(AnalysisDetailView ,self).get_context_data(**kwargs)
        context['dinamicmenu'] = dinamicMenu(self.kwargs['pk']) 
        return context
    

#------------------------------5w2h-----------------------------

class W5h2CreateView(UserPassesTestMixin,CreateView):
    model = W5h2
    template_name = 'w5h2/form.html'
    form_class = W5h2Form
    permission_denied_message = 'Você não pode adicionar um 5W2H! Você não tem a permição nescessaria ou não faz parte do time'
    
    def test_func(self):
        team_pk = Analysis.objects.get(pk= self.kwargs['analysis']).team.pk
        return is_in_team_and_has_permission(self.request.user,team_pk,'aqf.add_w5h2') 

    def form_valid(self , form):
        obj = form.save(commit = False)
        obj.analysis = Analysis.objects.get(pk= self.kwargs['analysis'])
        obj.criado_por = self.request.user
        obj.save()
        return super().form_valid(form)  

class W5h2DetailView(UserPassesTestMixin,DetailView):
    model =  W5h2
    template_name = 'w5h2/detail_card.html'
    permission_denied_message = 'Você não pode ver esse 5W2H! Você não tem a permição nescessaria ou não faz parte do time'
    
    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().analysis.team.pk,'aqf.view_w5h2') 

class W5h2EditView(UserPassesTestMixin,UpdateView):
    model = W5h2
    template_name = 'w5h2/form.html'
    form_class = W5h2Form
    permission_denied_message = 'Você não pode editar esse 5W2H! Você não tem a permição nescessaria ou não faz parte do time'

    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().analysis.team.pk,'aqf.change_w5h2') 

#--------------------------ishikawa---------------------

class IshikawaItems(UserPassesTestMixin,ListView):
    model = Ishikawa
    template_name = 'ishikawa/fish.html'
    permission_denied_message = 'Você não pode ver o Ishikawa! Você não tem a permição nescessaria ou não faz parte do time'

    def test_func(self):
        team_pk = Analysis.objects.get(pk= self.kwargs['analysis']).team.pk
        return is_in_team_and_has_permission(self.request.user,team_pk,'aqf.view_ishikawa') 

    def get_context_data(self, **kwargs):
        context = super(IshikawaItems ,self).get_context_data(**kwargs)
        try:
            context['componente'] =  W5h2.objects.get(analysis__pk =self.kwargs['analysis'] ).componete_pos_intervencao
        except ObjectDoesNotExist :
            context['componente'] = 'Não expecificado'
        return context 
    
    def get_queryset(self):
        object_list = Ishikawa.objects.filter(analysis__pk = self.kwargs['analysis'])
        return object_list

class IshikawaNew(UserPassesTestMixin,CreateView):
    model = Ishikawa
    template_name = 'ishikawa/modal.html'
    form_class = IshikawaForm
    permission_denied_message = 'Você não pode adicionar item ao Ishikawa! Você não tem a permição nescessaria ou não faz parte do time'

    def test_func(self):
        team_pk = Analysis.objects.get(pk= self.kwargs['analysis']).team.pk
        return is_in_team_and_has_permission(self.request.user,team_pk,'aqf.add_ishikawa') 
    
    def form_valid(self , form):
        obj = form.save(commit = False)
        obj.analysis = Analysis.objects.get(pk =self.kwargs['analysis'])
        obj.save()
        return JsonResponse({'msg':'seved'})

class IshikawaEditView(UserPassesTestMixin,UpdateView):
    model = Ishikawa
    template_name = 'ishikawa/edit.html'
    fields = ['categoria','procedencia','descricao']
    permission_denied_message = 'Você não pode editar item do Ishikawa! Você não tem a permição nescessaria ou não faz parte do time'

    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().analysis.team.pk,'aqf.change_ishikawa') 

    def form_valid(self , form):
        obj = form.save(commit = False)
        obj.save()
        return super().form_valid(form)


def ishikawaView(request,analysis):
    data = {'analysis': analysis ,'dinamicmenu' : dinamicMenu(analysis)}
    return render(request,'ishikawa/detail.html',data)

def ishikawaGenereteWhays(request,analysis):
    ishikawas = Ishikawa.objects.filter(analysis__pk = analysis )
    ishikawaWithWhays = Pqs5.objects.filter(analysis__pk = analysis).exclude( ishikawa__isnull= True).values_list('ishikawa__pk' ,flat=True)
    if not is_in_team_and_has_permission(request.user,Analysis.objects.get(pk=analysis).team.pk,'aqf.add_pqs5'):
        raise PermissionDenied("Você não adicionar item ao 5 porquês ! Você não tem a permição nescessaria ou não faz parte do time")
    for ishikawa in ishikawas:
        if (ishikawa.pk not in ishikawaWithWhays and ishikawa.procedencia == 3):
            Pqs5(analysis = Analysis.objects.get(pk=analysis),ishikawa = ishikawa).save()
            messages.success(request, 'Criado para {}'.format(ishikawa.descricao))      
    return redirect('pqs5_list', analysis=analysis)




#--------------------------Whays--------------------- 

class WhaysListView(UserPassesTestMixin,ListView):
    model =  Pqs5
    template_name = 'whays/list.html'
    permission_denied_message = 'Você não pode ver o 5 porquês! Você não tem a permição nescessaria ou não faz parte do time'

    def test_func(self):
        team_pk = Analysis.objects.get(pk=self.kwargs['analysis']).team.pk
        return is_in_team_and_has_permission(self.request.user,team_pk,'aqf.view_pqs5') 

    def get_context_data(self, **kwargs):
        context = super(WhaysListView, self).get_context_data(**kwargs)
        context['analysis'] =  self.kwargs['analysis']
        context['dinamicmenu'] = dinamicMenu(self.kwargs['analysis'])
        return context

    def get_queryset(self):
        object_list = Pqs5.objects.filter(analysis__pk = self.kwargs['analysis'])
        return object_list

class whaysNew(UserPassesTestMixin,CreateView):
    modal = Pqs5
    template_name = 'whays/form.html'
    form_class = Psq5Form
    permission_denied_message = 'Você não pode adicionar item ao 5 porquês! Você não tem a permição nescessaria ou não faz parte do time'

    def test_func(self):
        team_pk = Analysis.objects.get(pk=self.kwargs['analysis']).team.pk
        return is_in_team_and_has_permission(self.request.user,team_pk,'aqf.add_pqs5')

    def get_form_kwargs(self):
        kwargs = super(whaysNew, self).get_form_kwargs()
        kwargs['analysis'] = self.kwargs['analysis']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(whaysNew, self).get_context_data(**kwargs)
        context['form_type'] =  'new'
        return context
    
    def form_valid(self , form):
        obj = form.save(commit = False)
        obj.analysis = Analysis.objects.get(pk =self.kwargs['analysis'])
        obj.save()
        return JsonResponse({'msg':'seved'})

class whaysEditView(UserPassesTestMixin,UpdateView):
    model = Pqs5
    template_name = 'whays/form.html'
    form_class = Psq5Form
    permission_denied_message = 'Você não pode editar item do 5 porquês! Você não tem a permição nescessaria ou não faz parte do time'

    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().analysis.team.pk,'aqf.change_pqs5')

    def get_context_data(self, **kwargs):
        context = super(whaysEditView, self).get_context_data(**kwargs)
        context['form_type'] =  'update'
        return context

    def get_form_kwargs(self):
        kwargs = super(whaysEditView, self).get_form_kwargs()
        kwargs['analysis'] = Pqs5.objects.get(pk = self.kwargs['pk']).analysis.pk
        return kwargs

    def form_valid(self , form):
        obj = form.save(commit = False)
        obj.save()
        return JsonResponse({'msg':'seved'})

class WhaysTableView(UserPassesTestMixin,ListView):
    model =  Pqs5
    template_name = 'whays/table.html'
    permission_denied_message = 'Você não pode ver o 5 porquês! Você não tem a permição nescessaria ou não faz parte do time'

    def test_func(self):
        team_pk = Analysis.objects.get(pk=self.kwargs['analysis']).team.pk
        return is_in_team_and_has_permission(self.request.user,team_pk,'aqf.view_pqs5') 

    def get_queryset(self):
        object_list = Pqs5.objects.filter(analysis__pk = self.kwargs['analysis'])
        return object_list

class whaysDeleteView(UserPassesTestMixin,DeleteView):
    model = Pqs5
    template_name = 'generic/delete.html'
    form_class = Psq5Form
    permission_denied_message = 'Você não pode deletar item do 5 porquês! Você não tem a permição nescessaria ou não faz parte do time'

    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().analysis.team.pk,'aqf.delete_pqs5')

    def get_success_url(self):
        analysis = Pqs5.objects.get(pk = self.kwargs['pk'])
        analysis = analysis.id
        return reverse_lazy('pqs5_list',kwargs ={'analysis':analysis})

#-------------------------action-plan

class ActionListView(UserPassesTestMixin,ListView):
    model =  Acao
    template_name = 'action/list.html'
    permission_denied_message = 'Você não pode ver o plano de ação! Você não tem a permição nescessaria ou não faz parte do time'

    def test_func(self):
        team_pk = Analysis.objects.get(pk=self.kwargs['analysis']).team.pk
        return is_in_team_and_has_permission(self.request.user,team_pk,'aqf.view_acao')

    def get_context_data(self, **kwargs):
        context = super(ActionListView, self).get_context_data(**kwargs)
        context['buckets'] = Bucket.objects.all()
        return context

    def get_queryset(self):
        object_list = Acao.objects.filter(analysis__pk = self.kwargs['analysis'])
        return object_list

def Kamban(request,analysis):
    if not is_in_team_and_has_permission(request.user,Analysis.objects.get(pk=analysis).team.pk,'aqf.view_acao'):
        raise PermissionDenied("Você não pode ver o plano de ação! Você não tem a permição nescessaria ou não faz parte do time")
    buckets = Bucket.objects.all()
    data = {'buckets':buckets,'analysis':analysis,'dinamicmenu' : dinamicMenu(analysis)}
    return render(request,'action/kamban.html',data)

def apiActions(request,analysis):
    if not is_in_team_and_has_permission(request.user,Analysis.objects.get(pk=analysis).team.pk,'aqf.view_acao'):
        raise PermissionDenied("Você não pode ver o plano de ação! Você não tem a permição nescessaria ou não faz parte do time")
    json = []
    tasks = Acao.objects.filter(analysis__pk = analysis)
    for task in tasks:
        json.append(
                    {
                        "model": "aqf.acao",
                        "pk": task.pk,
                        "fields": {
                            "analysis": task.analysis.pk,
                            "bucket": task.bucket.pk,
                            "titulo": task.titulo,
                            "oque": task.oque,
                            "quando_inicio": task.quando_inicio.strftime('%d/%m/%Y %H:%M'),
                            "quando_fim": task.quando_fim.strftime('%d/%m/%Y %H:%M') if task.quando_fim else '',
                            "quem": task.quem.first_name if task.quem else 'Não atribuido',
                            "whays": task.whays.pk if (task.whays) else 0
                        }
                    }
                    )
    return JsonResponse(json, safe=False)


def apiActionChangeBucket(request):
    if request.method == "POST":
        task = request.POST.get('task').replace('task-','')
        to = request.POST.get('to')
        acao = Acao.objects.get(pk=int(task))
        if not is_in_team_and_has_permission(request.user,acao.analysis.team.pk,'aqf.change_acao'):
            raise PermissionDenied("Você não pode altera uama ação! Você não tem a permição nescessaria ou não faz parte do time")
        acao.bucket = Bucket.objects.get(pk=to)
        acao.save(update_fields=["bucket"])
        return JsonResponse({'msg':'saved'})

class ActionNew(UserPassesTestMixin,CreateView):
    model = Acao
    template_name = 'action/form.html'
    form_class = AcaoForm
    permission_denied_message = 'Você não pode adicionar ação! Você não tem a permição nescessaria ou não faz parte do time'

    def test_func(self):
        team_pk = Analysis.objects.get(pk=self.kwargs['analysis']).team.pk
        return is_in_team_and_has_permission(self.request.user,team_pk,'aqf.add_acao')

    def form_valid(self , form):
        obj = form.save(commit = False)
        obj.analysis = Analysis.objects.get(pk =self.kwargs['analysis'])
        obj.save()
        return JsonResponse({'msg':'seved','task':model_to_dict(obj)})

    def get_initial(self):
        bucket = self.request.GET.get('bucket',None)
        if  bucket :
            data = { 'bucket': Bucket.objects.get(pk = bucket) }
            return data

    def get_form_kwargs(self):
        kwargs = super(ActionNew, self).get_form_kwargs()
        kwargs['analysis'] = self.kwargs['analysis']
        return kwargs

class ActionEditView(UserPassesTestMixin,UpdateView):
    model = Acao
    template_name = 'action/edit_form.html'
    form_class = AcaoForm
    permission_denied_message = 'Você não pode editar uma ação! Você não tem a permição nescessaria ou não faz parte do time'

    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().analysis.team.pk,'aqf.change_acao')

    def get_form_kwargs(self):
        kwargs = super(ActionEditView, self).get_form_kwargs()
        kwargs['analysis'] = Acao.objects.get(pk = self.kwargs['pk']).analysis.pk
        return kwargs

    def get_success_url(self):
        acao = Acao.objects.get(pk = self.kwargs['pk'])
        analysis = acao.analysis.pk
        return reverse_lazy('kamban',kwargs ={'analysis':analysis})

class ActionDeleteView(UserPassesTestMixin,DeleteView):
    model = Acao
    template_name = 'generic/delete.html'
    permission_denied_message = 'Você não pode deletar uma ação! Você não tem a permição nescessaria ou não faz parte do time'

    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().analysis.team.pk,'aqf.delete_acao')

    def get_success_url(self):
        analysis = Acao.objects.get(pk = self.kwargs['pk'])
        analysis = analysis.id
        return reverse_lazy('kamban',kwargs ={'analysis':analysis})
#-------------------------

class ShiftList(ListView):
    model = Shift
    template_name = 'shift/list.html'
    


    def get_queryset(self):
        object_list = Shift.objects.filter(team__pk = self.kwargs['team'])
        return object_list    

class ShiftCreate(UserPassesTestMixin,CreateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'generic/form.html'
    permission_denied_message = 'Você não pode alterar esse time!'

    def test_func(self):
        team = self.request.POST.get('team') if self.request.GET.get('team',None) is None else self.request.GET.get('team')
        return is_in_team_and_has_permission(self.request.user,team,'accounts.change_team')

    def get_initial(self):
        team= self.request.GET.get('team',None)
        if  team :
            data = { 'team': Team.objects.get(pk = team) }
            return data

    def get_form_kwargs(self):
        kwargs = super(ShiftCreate, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        obj = form.save(commit = False)
        obj.save()
        return JsonResponse({'msg':'saved'})

class ShiftDelete(UserPassesTestMixin,DeleteView):
    model = Shift
    template_name = 'generic/delete.html'
    success_url = reverse_lazy('myteams')
    permission_denied_message = 'Você não pode alterar esse time!'

    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().team.pk,'accounts.change_team')

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except RestrictedError:
            messages.error(request, "O turno não pode ser deletado pois existem analises usando-o")
            return redirect(reverse_lazy('myteams'))


class AreaList(ListView):
    model = Area
    template_name = 'area/list.html'

    def get_queryset(self):
        object_list = Area.objects.filter(team__pk = self.kwargs['team'])
        return object_list    

class CreateArea(UserPassesTestMixin,CreateView):
    model = Area
    form_class = AreaForm
    template_name = 'generic/form.html'
    permission_denied_message = 'Você não pode alterar esse time!'

    def test_func(self):
        team = self.request.POST.get('team') if self.request.GET.get('team',None) is None else self.request.GET.get('team')
        return is_in_team_and_has_permission(self.request.user,team,'accounts.change_team')

    def get_form_kwargs(self):
        kwargs = super(CreateArea, self).get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs

    def get_initial(self):
        team= self.request.GET.get('team',None)
        if  team :
            data = { 'team': Team.objects.get(pk = team) }
            return data
    
    def form_valid(self, form):
        obj = form.save(commit = False)
        obj.save()
        return JsonResponse({'msg':'saved'})

class AreaDelete(UserPassesTestMixin,DeleteView):
    model = Area
    template_name = 'generic/delete.html'
    success_url = reverse_lazy('myteams')
    permission_denied_message = 'Você não pode alterar esse time!'

    def test_func(self):
        return is_in_team_and_has_permission(self.request.user,self.get_object().team.pk,'accounts.change_team')


    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except RestrictedError:
            messages.error(request, "A área não pode ser deletada pois existem analises usando-a")
            return redirect(reverse_lazy('myteams'))

#############################################################################################################################################################################


