from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse 
from accounts.models import Team
# Create your models here
class Area(models.Model):
        description = models.CharField(max_length=150)
        team = models.ForeignKey(Team,on_delete= models.CASCADE)
        def __str__(self):
                return str(self.description)

class Shift(models.Model):
        description = models.CharField(max_length=150)
        team = models.ForeignKey(Team,on_delete= models.RESTRICT)
        def __str__(self):
                return str(self.description)

class Analysis(models.Model):
        problem_description =  models.CharField(max_length=250)
        do_w5h2 = models.BooleanField(default=True)
        do_ishikawa = models.BooleanField(default= True)
        do_whays = models.BooleanField(default=True)
        do_action_plan = models.BooleanField(default=True)
        team = models.ForeignKey(Team,on_delete= models.RESTRICT)
        area= models.ForeignKey(Area, on_delete= models.RESTRICT)
        shift = models.ForeignKey(Shift, on_delete= models.RESTRICT) 
        members = models.ManyToManyField(User,related_name='member_analysis_set')
        created_by = models.ForeignKey(User,related_name='creator_analysis_set',on_delete= models.RESTRICT)

        def has_open_ishikawa(self):
                if Ishikawa.objects.filter(analysis= self).exclude(procedencia=2 ):
                        return True
                else:
                        return False

        def has_ishikawa(self):
                if Ishikawa.objects.filter(analysis= self):
                        return True
                else:
                        return False

        def __str__(self):
                return str(self.problem_description)

        def get_absolute_url(self):
                return reverse('analysis_detail',args = [self.pk])
        
class W5h2(models.Model): 
    status_list = (
            (1,'Criada'),
            (2,'Preenchida'),
            (3,'Revisada'),
            (4,'Finalizada'),
            )

    analysis = models.OneToOneField(Analysis,on_delete= models.CASCADE)
    componente = models.CharField(max_length = 250,null = True) 

    oque = models.TextField()
    onde = models.TextField()
    quando = models.TextField()
    quem = models.TextField()
    qual = models.TextField()
    como = models.TextField()

    
    componete_pos_intervencao = models.CharField(max_length = 100)
    modo_falha = models.CharField(max_length = 100)
    
    status = models.IntegerField( choices = status_list, default =1)
    
    criado_por = models.ForeignKey(User,on_delete= models.CASCADE)
    
    def get_absolute_url(self):
        return reverse('analysis_detail',args = [self.analysis.pk])
    
    def __str__(self):
        return str(self.pk)



class Ishikawa(models.Model):
    categorias = (
            ('metodo','METODO'),
            ('materiais','MATERIAIS'),
            ('mao_de_obra','MÃO-DE-OBRA'),
            ('maquina','MAQUINA'),
            ('meio_amb','MEIO AMBIENTE'),
            ('medicao','MEDIÇÃO'),
            )
    
    procedencias = (
            (1,'NÃO PROCEDE'),
            (2,'EM ANÁLISE'),
            (3,'PROCEDE'),
            )
    
    analysis = models.ForeignKey(Analysis, on_delete= models.CASCADE)
    categoria = models.CharField(max_length = 50 ,choices = categorias)
    procedencia = models.BigIntegerField( choices = procedencias, default= 2)
    descricao =   models.CharField(max_length = 250)
    
    def __str__(self):
        return str(self.descricao)

    def get_absolute_url(self):
        return reverse('ishikawa_view',args = [self.analysis.pk])

class Pqs5(models.Model):
    analysis = models.ForeignKey(Analysis, on_delete= models.CASCADE)
    ishikawa = models.ForeignKey(Ishikawa, on_delete= models.CASCADE, null = True, blank = True)
    pq1 = models.CharField(max_length = 250, null = True, blank = True)
    pq2 = models.CharField(max_length = 250, null = True, blank = True)
    pq3 = models.CharField(max_length = 250, null = True, blank = True)
    pq4 = models.CharField(max_length = 250, null = True, blank = True)
    pq5 = models.CharField(max_length = 250, null = True, blank = True)
    
    def __str__(self):
        return str(self.pq1)
    
    
class Bucket(models.Model):
        name = models.CharField(max_length=20)
        is_done = models.BooleanField() 
        
        def __str__(self):
                return str(self.name)
    
class Acao(models.Model):

    analysis = models.ForeignKey(Analysis,on_delete = models.CASCADE)
    bucket = models.ForeignKey(Bucket, on_delete= models.RESTRICT)
    titulo = models.CharField(max_length=150)
    oque =  models.TextField(null=True,blank=True)
    quando_inicio = models.DateTimeField(default=timezone.now(),null=True,blank=True) # mudar para obrigatorio
    quando_fim = models.DateTimeField(default=timezone.now(),null=True,blank=True) 
    quem =  models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True)
    whays = models.ForeignKey(Pqs5,on_delete= models.CASCADE,null=True,blank=True)

    
    def __str__(self):
        return str(self.titulo)   
    
    


    
    
    
    
    
    
    


    
   
    