# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 15:15:15 2020

@author: italo
"""

from django.forms import ModelForm
from .models import Analysis,Pqs5, Ishikawa, Acao,W5h2 , Shift , Area
from accounts.models import Team
from django.db.models import Q 
from django.contrib.auth.models import User

class Psq5Form(ModelForm):
    class Meta:
        model = Pqs5
        exclude = ['analysis']
        labels = {
        'pq1':('1°Porquê'),
        'pq2':('2°Porquê'),
        'pq3':('3°Porquê'),
        'pq4':('4°Porquê'),
        'pq5':('5°Porquê'),
        }
    def __init__(self, *args, **kwargs):
        analysis = kwargs.pop('analysis')
        super().__init__(*args, **kwargs)
        self.fields['pq1'].required = True
        self.fields['ishikawa'].queryset = Ishikawa.objects.filter(analysis__pk = analysis)
        
class IshikawaForm(ModelForm):
    class Meta:
        model = Ishikawa
        #fields = '__all__'
        fields = ('categoria','procedencia','descricao')   
     
        
class AcaoForm(ModelForm):
    class Meta:
        model = Acao
        exclude = ['analysis']
        labels = {
        'whays':('5°Porquê '),
        'oque':('O que '),
        }
        help_texts = {
            'whays': ('item que gerou a ação'),
        }

    def __init__(self, *args, **kwargs):
        analysis = kwargs.pop('analysis')
        super(AcaoForm, self).__init__(*args, **kwargs)
        self.fields['quem'].queryset = User.objects.filter(pk__in = Analysis.objects.get(pk=analysis).members.all())
        self.fields['whays'].queryset = Pqs5.objects.filter(analysis__pk = analysis)


class AnalysisForm(ModelForm):
    class Meta:           
        model = Analysis
        exclude = ['created_by']
        labels = {
        'problem_description':('Descrição do problema'),
        'do_w5h2':('Fazer 5W2H'),
        'do_ishikawa':('Fazer Ishikawa'),
        'do_whays':('Fazer 5 porquês'),
        'do_action_plan':('Fazer plano de ação'),
        'team':('Time'),
        'area':('Area'),
        'shift':('Turno'),
        'members':('Membros'),
        }

        help_texts = {
            'members': ('Pressione “Control”, ou “Command” no Mac, para selecionar mais de um).'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('current_user')
        super(AnalysisForm, self).__init__(*args, **kwargs)
        teams = Team.objects.filter(Q(function__member__user = user) | Q(owner= user) ).distinct()
        self.fields['team'].queryset = teams
        self.fields['shift'].queryset = Shift.objects.filter(team__in=teams)
        self.fields['area'].queryset = Area.objects.filter(team__in=teams)
        self.fields['members'].queryset = User.objects.filter(member__function__team__in = teams)

class W5h2Form(ModelForm):
    class Meta:           
        model = W5h2
        exclude = ['analysis','criado_por','status']
        labels = {
        'oque':('O que '),
        'componete_pos_intervencao':('Componente pós-intervenção'),
        }
        help_texts = {
            'oque': ('O que foi encontrado de problema após a análise inicial do modo falha? (Exemplos: rolamento travado, viscosidade do material, baixa tensão.).'),
            'onde': ('Localização da falha, local do equipamento ou componente, ou material onde ocorre a falha (Exemplo: Sistema de regeneração, agitador traseiro do tanque 1, mancal dianteiro do motor, conector traseiro da IHM, sistema hidráulico.).'),
            'quando': ('Descrição do momento de ocorrência da falha, relacionado ao processo produtivo (Exemplo: em operação normal, em reinício de produção, durante o retorno de manutenção corretiva, durante o retorno de manutenção programada, durante despressurização do processo, durante retorno pós-falta de energia, durante ajuste operacional) e/ou ciclo do equipamento (Exemplo: no momento de dobra do cartucho, no momento de inserção dos cartuchos na caixa, no momento de fechamento do molde, no momento de avanço do empurrador). Para os casos de reinício ou retorno de parada (paradas corretivas, paradas preventivas, intervenções para ajuste), considera-se o seguinte: após a máquina entrar em regime/velocidade nominal e produzir 60 minutos, considera-se operação normal. Antes disto, ainda faz parte da parada.'),
            'quem': ('Pode estar relacionado à habilidade do operador, técnico de manutenção ou técnico de instalação. Em alguma atividade da rotina realizada pelo colaborador (operador, técnico de manutenção ou instalação), este pode realizar alguma intervenção que possa ser a causa da quebra/falha. Exemplos: ajustes operacionais (operador), qualidade de serviço de reparo/manutenção anteriormente executado (técnico de manutenção), ajustes funcionais (técnico de manutenção) ou qualidade e o serviço de instalação do equipamento anteriormente executado (técnico de instalação), ausência ou excesso de lubrificante (técnico de manutenção).'),
            'qual': ('Existe tendência de reincidência da falha. Duas visões devem ser analisadas: 1. Histórica: este problema já ocorreu (buscar histórico para a máquina - 6 meses) e reincidiu no passado por um mesmo motivo. 2. Futura: existem outros equipamentos/conjunto/subconjunto na instalação que operam na mesma condição (mesmo produto, velocidade, carga e regime de trabalho).'),
            'como': ('Descrição de como ocorre a falha, como o equipamento muda do estado normal para o anormal, ou seja, o que fez a produção acionar a manutenção. (Exemplo: desarme do motor (falha: rolamento travado), vazamento de óleo (falha: retentor danificado), parada do motor (falha: cabo em curto-circuito), parada do agitador (falha: quebra do eixo), parada de comunicação da rede (falha: cabo de rede rompido).'),

        }
        
class AreaForm(ModelForm):
    class Meta:           
        model = Area
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('current_user')
        super(AreaForm, self).__init__(*args, **kwargs)
        team = Team.objects.filter(Q(function__member__user = user) | Q(owner= user) ).distinct()
        self.fields['team'].queryset = team
        
class ShiftForm(ModelForm):
    class Meta:           
        model = Shift
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('current_user')
        super(ShiftForm, self).__init__(*args, **kwargs)
        team = Team.objects.filter(Q(function__member__user = user) | Q(owner= user) ).distinct()
        self.fields['team'].queryset = team            